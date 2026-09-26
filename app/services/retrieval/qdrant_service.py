import logfire
from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.config import settings
from app.services.retrieval.embedding import embed_query


client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)


def search_enterprise_knowledge(
    query: str,
    limit: int = 8,
    user_role: str = "clinician",
):
    """
    Semantic retrieval with document-level role-based access control.
    """

    try:
        query_vector = embed_query(query)

        query_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="allowed_roles",
                    match=models.MatchValue(value=user_role),
                    
                )
            ]
        )

        response = client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
        )

        results = []

        for res in response.points:
            payload = res.payload or {}

            results.append(
                {
                    "content": payload.get("text", ""),
                    "source": payload.get("source", "Unknown"),
                    "source_type": payload.get("source_type", "Unknown"),
                    "document_id": payload.get("document_id"),
                    "title": payload.get("title"),
                    "document_type": payload.get("document_type"),
                    "version": payload.get("version"),
                    "status": payload.get("status"),
                    "effective_date": payload.get("effective_date"),
                    "supersedes": payload.get("supersedes"),
                    "chunk_index": payload.get("chunk_index"),
                    "row_number": payload.get("row_number"),
                    "score": res.score,
                }
            )

        return results

    except Exception as e:
        logfire.error(f"Qdrant Search Failed: {e}")
        return []