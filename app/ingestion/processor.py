import os
import sys
import uuid
import json
import csv
import re
import logfire

from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.config import settings
from app.services.retrieval.embedding import embed_texts, get_embedding_dim

from app.ingestion.loaders.pdf import parse_pdf
from app.ingestion.loaders.html import parse_html
from app.ingestion.loaders.text import parse_text
from app.ingestion.chunking.splitter import chunk_text


logfire.configure(
    service_name="enterprise-ingestion-service",
    send_to_logfire=False,
)

PROCESSED_DATA_DIR = "processed_data"

qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)


# ============================================================
# HEALTHCARE METADATA
# ============================================================

ROLE_MAP = {
    "guidelines": ["clinician", "admin"],
    "policies": ["clinician", "nurse", "operations", "admin"],
    "sop": ["clinician", "nurse", "admin"],
    "devices": ["clinician", "biomedical_engineer", "admin"],
    "formulary": ["clinician", "nurse", "operations", "admin"],
    "restricted": ["clinician", "admin"],
    "operational": ["operations", "admin"],
}


def extract_metadata(text: str, filename: str, source_type: str) -> dict:
    """
    Extract healthcare document metadata from the document header.
    """

    def extract(pattern, default=None):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else default

    return {
        "document_id": extract(
            r"Document ID:\s*(.+)", filename
        ),
        "title": extract(
            r"Title:\s*(.+)", filename
        ),
        "version": extract(
            r"Version:\s*(.+)", "1.0"
        ),
        "status": extract(
            r"Status:\s*(.+)", "ACTIVE"
        ),
        "effective_date": extract(
            r"Effective date:\s*(.+)", None
        ),
        "supersedes": extract(
            r"Superseded by:\s*(.+)",
            extract(r"Supersedes:\s*(.+)", None)
        ),
        "document_type": extract(
            r"Document type:\s*(.+)", source_type
        ),
        "allowed_roles": ROLE_MAP.get(
            source_type,
            ["admin"]
        ),
    }


def save_processed_locally(
    data: dict,
    source_type: str,
    filename: str
) -> str:
    """Save parsed chunk metadata locally."""

    folder = os.path.join(
        PROCESSED_DATA_DIR,
        source_type
    )

    os.makedirs(folder, exist_ok=True)

    safe_filename = filename.replace("/", "_")

    dest = os.path.join(
        folder,
        f"{safe_filename}.json"
    )

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    return dest


# ============================================================
# CSV / TABLE PROCESSING
# ============================================================

def parse_csv_rows(file_path: str):
    """
    Convert every CSV row into an independent searchable chunk.

    This is important because table evidence should be traceable
    to an individual row rather than one giant CSV document.
    """

    rows = []

    with open(
        file_path,
        "r",
        encoding="utf-8",
        newline=""
    ) as f:

        reader = csv.DictReader(f)

        for index, row in enumerate(reader, start=1):

            row_text = " | ".join(
                f"{key}: {value}"
                for key, value in row.items()
            )

            rows.append({
                "row_number": index,
                "text": row_text,
            })

    return rows


# ============================================================
# FILE PROCESSING
# ============================================================

def process_file(
    file_path: str,
    filename: str,
    source_type: str
):

    with logfire.span(
        "Processing File",
        file=filename,
        source=source_type
    ):

        try:

            ext = filename.lower().rsplit(".", 1)[-1]

            # ------------------------------------------------
            # CSV — ROW LEVEL INGESTION
            # ------------------------------------------------

            if ext == "csv":

                rows = parse_csv_rows(file_path)

                if not rows:
                    logfire.warning(
                        f"No rows found in {filename}"
                    )
                    return

                # CSV has no header metadata,
                # so create controlled metadata.
                metadata = {
                    "document_id": filename.rsplit(".", 1)[0],
                    "title": filename,
                    "version": "1.0",
                    "status": "ACTIVE",
                    "effective_date": None,
                    "supersedes": None,
                    "document_type": "Table / Formulary",
                    "allowed_roles": ROLE_MAP["formulary"],
                }

                chunks = [
                    row["text"]
                    for row in rows
                ]

                row_numbers = [
                    row["row_number"]
                    for row in rows
                ]

            # ------------------------------------------------
            # NORMAL DOCUMENTS
            # ------------------------------------------------

            else:

                if ext == "pdf":
                    full_text = parse_pdf(file_path)

                elif ext in ("html", "htm"):
                    full_text = parse_html(file_path)

                elif ext == "txt":
                    full_text = parse_text(file_path)

                elif ext in ("docx", "pptx"):
                    from app.ingestion.loaders.office import parse_office
                    full_text = parse_office(file_path)

                else:
                    logfire.warning(
                        f"Skipping unsupported file type: {filename}"
                    )
                    return

                if not full_text or not full_text.strip():
                    logfire.warning(
                        f"No text extracted from {filename}"
                    )
                    return

                metadata = extract_metadata(
                    full_text,
                    filename,
                    source_type
                )

                chunks = chunk_text(full_text)

                if not chunks:
                    return

                row_numbers = [None] * len(chunks)

            # ------------------------------------------------
            # CREATE CITABLE CHUNKS
            # ------------------------------------------------

            enriched_chunks = []

            for index, (chunk, row_number) in enumerate(
                zip(chunks, row_numbers),
                start=1
            ):

                chunk_id = (
                    f"{metadata['document_id']}"
                    f"_v{metadata['version']}"
                    f"_c{index}"
                )

                enriched_chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk,
                    "chunk_index": index,
                    "row_number": row_number,
                })

            # ------------------------------------------------
            # SAVE PROCESSED DATA
            # ------------------------------------------------

            processed_data = {
                "filename": filename,
                "source_type": source_type,
                "metadata": metadata,
                "chunks": enriched_chunks,
            }

            local_path = save_processed_locally(
                processed_data,
                source_type,
                filename
            )

            logfire.info(
                f"Saved processed data → {local_path}"
            )

            # ------------------------------------------------
            # EMBEDDING
            # ------------------------------------------------

            texts = [
                item["text"]
                for item in enriched_chunks
            ]

            embeddings = embed_texts(texts)

            # ------------------------------------------------
            # QDRANT POINTS
            # ------------------------------------------------

            points = []

            for item, vector in zip(
                enriched_chunks,
                embeddings
            ):

                payload = {
                    "chunk_id": item["chunk_id"],
                    "text": item["text"],

                    "source": filename,
                    "source_type": source_type,

                    "document_id": metadata["document_id"],
                    "title": metadata["title"],
                    "document_type": metadata["document_type"],

                    "version": metadata["version"],
                    "status": metadata["status"],
                    "effective_date": metadata["effective_date"],
                    "supersedes": metadata["supersedes"],

                    "allowed_roles": metadata["allowed_roles"],

                    "chunk_index": item["chunk_index"],
                    "row_number": item["row_number"],
                }

                points.append(
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload=payload,
                    )
                )

            # ------------------------------------------------
            # UPSERT
            # ------------------------------------------------

            qdrant_client.upsert(
                collection_name=settings.QDRANT_COLLECTION,
                points=points,
            )

            logfire.info(
                f"Indexed {len(points)} points "
                f"from {filename}"
            )

        except Exception as e:

            logfire.error(
                f"Failed to process {filename}: {e}"
            )

            raise


# ============================================================
# DIRECTORY PROCESSING
# ============================================================

def process_directory(
    dir_path: str,
    source_type: str
):

    with logfire.span(
        "Scanning Directory",
        path=dir_path,
        source=source_type
    ):

        files = [
            f
            for f in os.listdir(dir_path)
            if os.path.isfile(
                os.path.join(dir_path, f)
            )
        ]

        logfire.info(
            f"Found {len(files)} files in {dir_path}."
        )

        for filename in files:

            process_file(
                os.path.join(
                    dir_path,
                    filename
                ),
                filename,
                source_type
            )


# ============================================================
# UNIVERSAL INGESTION
# ============================================================

def run_universal_ingestion(
    base_dir: str,
    explicit_source_type: str = None,
    wipe: bool = False
):

    with logfire.span(
        "Universal Ingestion Started",
        base_directory=base_dir
    ):

        # ------------------------------------------------
        # WIPE COLLECTION
        # ------------------------------------------------

        if wipe:

            if qdrant_client.collection_exists(
                settings.QDRANT_COLLECTION
            ):

                qdrant_client.delete_collection(
                    settings.QDRANT_COLLECTION
                )

                logfire.info(
                    f"Collection "
                    f"'{settings.QDRANT_COLLECTION}' deleted."
                )

        # ------------------------------------------------
        # CREATE COLLECTION
        # ------------------------------------------------
        if not qdrant_client.collection_exists(
            settings.QDRANT_COLLECTION
        ):

            dim = get_embedding_dim()

            qdrant_client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=models.VectorParams(
                    size=dim,
                    distance=models.Distance.COSINE,
                ),
            )

            # Index allowed_roles for role-based filtering
            qdrant_client.create_payload_index(
                collection_name=settings.QDRANT_COLLECTION,
                field_name="allowed_roles",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )

            logfire.info(
                f"Created collection "
                f"'{settings.QDRANT_COLLECTION}' "
                f"({dim}-dim, Cosine)."
            )
        
        # ------------------------------------------------
        # DISCOVER SUBDIRECTORIES
        # ------------------------------------------------

        subdirs = [
            d
            for d in os.listdir(base_dir)
            if os.path.isdir(
                os.path.join(base_dir, d)
            )
        ]

        if not subdirs:

            source_type = (
                explicit_source_type
                or "general"
            )

            process_directory(
                base_dir,
                source_type
            )

        else:

            for subdir in subdirs:

                source_type = subdir.lower()

                process_directory(
                    os.path.join(
                        base_dir,
                        subdir
                    ),
                    source_type
                )


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    wipe_requested = "--wipe" in sys.argv

    clean_args = [
        a
        for a in sys.argv
        if a != "--wipe"
    ]

    target_dir = (
        clean_args[1]
        if len(clean_args) > 1
        else "DATA"
    )

    explicit_type = (
        clean_args[2]
        if len(clean_args) > 2
        else None
    )

    if not os.path.exists(target_dir):

        print(
            f"Error: path '{target_dir}' does not exist."
        )

        sys.exit(1)

    run_universal_ingestion(
        target_dir,
        explicit_source_type=explicit_type,
        wipe=wipe_requested
    )

    logfire.info(
        "Ingestion job completed."
    )