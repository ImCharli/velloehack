
````markdown
# Velloe Enterprise AI

> Enterprise-grade healthcare knowledge assistant built with LangGraph, RAG, Qdrant, NeMo Guardrails, LLM Gateway support, evaluation pipelines, and a Streamlit interface.

Velloe Enterprise AI is a grounded enterprise knowledge assistant designed to answer questions from internal healthcare documentation while providing retrieved evidence and maintaining a structured agent workflow.

The system combines **LangGraph orchestration**, **vector retrieval**, **reranking**, **guardrails**, **LLM generation**, **observability**, and **evaluation tooling** into a single RAG pipeline.

---

## Features

- 🧠 **LangGraph Agentic RAG**
  - Planner → Retriever → Responder workflow
  - Explicit intermediate state
  - Thread-based conversational memory

- 🔎 **Enterprise Retrieval**
  - Qdrant vector database
  - Embedding-based retrieval
  - FlashRank-based reranking
  - Context-grounded generation

- 🛡️ **AI Guardrails**
  - NeMo Guardrails
  - Off-topic request handling
  - Jailbreak protection
  - Controlled enterprise interaction

- 🚪 **LLM Gateway**
  - Gateway abstraction for model access
  - Portkey integration
  - Groq support
  - Configurable fallback architecture

- 📊 **Evaluation Framework**
  - Golden datasets
  - Retrieval and answer evaluation
  - Guardrail evaluation
  - Evaluation metrics
  - Automated evaluation pipeline

- 🔬 **Observability**
  - Pydantic Logfire
  - LangSmith integration
  - Agent execution tracing

- 🖥️ **Streamlit UI**
  - Clean enterprise interface
  - Role selection
  - Knowledge-base querying
  - Retrieved evidence display
  - Retrieval pipeline details

- 📚 **Multi-format ingestion**
  - PDF
  - HTML
  - TXT
  - CSV
  - DOCX
  - PPTX

---

# Architecture

```text
                         ┌──────────────────────┐
                         │    Streamlit UI      │
                         │  Enterprise Client   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │     /query API       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Guardrails        │
                         │   NeMo Guardrails    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      LangGraph       │
                         │    Agent Workflow    │
                         └──────────┬───────────┘
                                    │
                     ┌──────────────┼──────────────┐
                     ▼              ▼              ▼
              ┌────────────┐ ┌────────────┐ ┌────────────┐
              │  Planner   │ │ Retriever  │ │ Responder  │
              └────────────┘ └─────┬──────┘ └─────┬──────┘
                                   │              │
                                   ▼              │
                            ┌──────────────┐       │
                            │    Qdrant    │       │
                            │ Vector Store │       │
                            └──────┬───────┘       │
                                   │               │
                                   ▼               │
                            ┌──────────────┐       │
                            │  Reranking   │       │
                            │  FlashRank   │       │
                            └──────┬───────┘       │
                                   │               │
                                   └───────┬───────┘
                                           ▼
                                  ┌────────────────┐
                                  │      LLM       │
                                  │ Gateway / Model│
                                  └────────────────┘
````

---

# Example

### Query

```text
What is the recommended dose for Drug-A for an adult weighing more than 80kg?
```

### Response

```text
Based on the enterprise documentation, the recommended dose
for Drug-A for an adult weighing >80kg is 30mg.
```

### Retrieved evidence

```text
Medication: Drug-A
Population: Adult
Weight_Range: >80kg
Recommended_Dose: 30mg
Status: Active
Effective_Date: 2026-01-01
```



# Project Structure

```text
velloehack/
│
├── app/
│   ├── agents/
│   │   ├── graph.py
│   │   ├── state.py
│   │   └── nodes/
│   │       ├── planner.py
│   │       ├── retriever.py
│   │       └── responder.py
│   │
│   ├── gateway/
│   │   ├── __init__.py
│   │   └── client.py
│   │
│   ├── guardrails/
│   │   ├── __init__.py
│   │   ├── colang_rules.py
│   │   └── rails.py
│   │
│   ├── ingestion/
│   │   ├── chunking/
│   │   ├── loaders/
│   │   └── processor.py
│   │
│   ├── services/
│   │   └── retrieval/
│   │       ├── embedding.py
│   │       ├── qdrant_service.py
│   │       └── ranking_service.py
│   │
│   ├── config.py
│   └── main.py
│
├── DATA/
│   └── healthcare/
│       ├── devices/
│       ├── evaluation/
│       ├── formulary/
│       ├── guidelines/
│       ├── operational/
│       ├── policies/
│       ├── restricted/
│       └── sop/
│
├── DOCS/
│   ├── 01_SYSTEM_OVERVIEW.md
│   ├── 02_INGESTION_ENGINE.md
│   ├── 03_NODE_INTELLIGENCE.md
│   ├── 04_TRACING_AND_OBSERVABILITY.md
│   ├── 05_ENVIRONMENT_VARIABLES.md
│   ├── 06_KNOWN_GOTCHAS.md
│   ├── 07_FLASHRANK_RERANKING.md
│   ├── 08_GUARDRAILS.md
│   ├── 09_LLM_GATEWAY.md
│   ├── 10_EVALS.md
│   └── 11_EVALS_PIPELINE.md
│
├── evals/
│   ├── app.py
│   ├── data_parser.py
│   ├── guardrails_eval.py
│   ├── metrics.py
│   ├── pipeline.py
│   └── golden_dataset.json
│
├── streamlit_app.py
├── requirements.txt
├── requirements-prod.txt
├── Dockerfile
├── ARCHITECTURE.md
└── README.md
```

---

# Technology Stack

| Layer               | Technology                     |
| ------------------- | ------------------------------ |
| Frontend            | Streamlit                      |
| API                 | FastAPI                        |
| Agent Orchestration | LangGraph                      |
| Retrieval           | Qdrant                         |
| Reranking           | FlashRank                      |
| Guardrails          | NeMo Guardrails                |
| LLM Framework       | LangChain                      |
| LLM Gateway         | Portkey                        |
| LLM Provider        | Groq / configurable providers  |
| Embeddings          | Configurable embedding service |
| Observability       | Pydantic Logfire               |
| Tracing             | LangSmith                      |
| Evaluation          | Custom evaluation pipeline     |
| Containerization    | Docker                         |

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/ImCharli/velloehack.git
cd velloehack
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_FALLBACK_API_KEY=your_fallback_key

PORTKEY_API_KEY=your_portkey_api_key

LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=velloe-enterprise-ai

LOGFIRE_TOKEN=your_logfire_token
```



# Running the Backend

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API

## POST `/query`

Example request:

```bash
curl -X POST \
  http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "q": "What is the recommended dose for Drug-A for an adult weighing more than 80kg?",
    "thread_id": "demo-1"
  }'
```

Example response:

```json
{
  "question": "What is the recommended dose for Drug-A for an adult weighing more than 80kg?",
  "answer": "Based on the provided enterprise documentation, the recommended dose for Drug-A for an adult weighing >80kg is 30mg.",
  "thought_process": [
    "Intent: Enterprise Knowledge",
    "Search Term: Drug-A adult recommended dosage over 80kg",
    "Context Retrieved"
  ],
  "status": "Response generated.",
  "sources": [
    "Medication: Drug-A | Population: Adult | Weight_Range: >80kg | Recommended_Dose: 30mg | Status: Active | Effective_Date: 2026-01-01"
  ]
}
```

---

# Running the Streamlit UI

Start the backend first:

```bash
uvicorn app.main:app --reload
```

Then, in another terminal:

```bash
python -m streamlit run streamlit_app.py
```

The Streamlit application will open locally.

The UI communicates with the FastAPI backend through:

```text
POST /query
```

---

# RAG Pipeline

The core workflow is:

```text
User Query
    │
    ▼
Guardrails
    │
    ▼
Planner
    │
    ▼
Query Generation
    │
    ▼
Vector Retrieval
    │
    ▼
Qdrant
    │
    ▼
FlashRank Reranking
    │
    ▼
Relevant Context
    │
    ▼
LLM Responder
    │
    ▼
Grounded Answer
    │
    ▼
Evidence + Response
```



# Document Ingestion

The ingestion engine supports multiple document types.

```text
Documents
    │
    ▼
File Loader
    │
    ▼
Text Extraction
    │
    ▼
Chunking
    │
    ▼
Metadata
    │
    ▼
Embeddings
    │
    ▼
Qdrant
```

Supported formats include:

* PDF
* HTML
* TXT
* CSV
* DOCX
* PPTX

---

# Guardrails

NeMo Guardrails provides a control layer before requests reach the main RAG workflow.

The guardrail layer is intended to handle:

* Off-topic requests
* Jailbreak attempts
* Unsupported conversational requests
* Controlled enterprise interactions

The guardrail implementation is located in:

```text
app/guardrails/
```

---

# Evaluation

The repository contains an evaluation framework for measuring system behavior.

```text
evals/
├── golden_dataset.json
├── data_parser.py
├── metrics.py
├── guardrails_eval.py
├── pipeline.py
└── app.py
```

The evaluation pipeline can be used to test:

* Retrieval quality
* Answer quality
* Grounding
* Guardrail behavior
* Golden dataset performance

Run the evaluation workflow according to the scripts documented in:

```text
DOCS/10_EVALS.md
DOCS/11_EVALS_PIPELINE.md
```

---

# Observability

The system supports application tracing and observability through:

### Pydantic Logfire

Used for application and agent execution observability.

### LangSmith

Used for tracing LangChain/LangGraph execution.

These integrations are configurable through environment variables.

---

# Security

The project follows several basic security practices:

* API keys are loaded through environment variables.
* `.env` is excluded from Git.
* Secrets are not stored in source code.
* Role information can be used for access-control decisions.
* Guardrails are applied before the RAG pipeline.
* Enterprise context is separated from the model's general knowledge.

Before production deployment, additional authentication, authorization, audit logging, rate limiting, and secret management should be configured.

---

# Design Principles

### 1. Grounded Generation

Answers should be based on retrieved enterprise documentation.

### 2. Traceability

The system exposes retrieved sources alongside generated answers.

### 3. Modular Architecture

Planner, retrieval, ranking, generation, ingestion, and guardrails are separated into independent modules.

### 4. Evaluation-Driven Development

The system includes a dedicated evaluation pipeline instead of relying only on manual testing.

### 5. Provider Flexibility

LLM access is abstracted so providers can be changed without rewriting the complete application.

---

# Known Limitations

This project is currently a demonstration/prototype and should not be treated as a production clinical decision-support system.

Production deployment would require additional work around:

* Authentication
* Authorization
* Audit logging
* Secrets management
* Rate limiting
* Data governance
* PHI handling
* Monitoring and alerting
* Retrieval evaluation at production scale
* LLM reliability and fallback handling
* Clinical validation

---

# Documentation

Detailed technical documentation is available under:

```text
DOCS/
```

Important documents:

* `01_SYSTEM_OVERVIEW.md` — System architecture
* `02_INGESTION_ENGINE.md` — Document ingestion
* `03_NODE_INTELLIGENCE.md` — Agent nodes
* `04_TRACING_AND_OBSERVABILITY.md` — Observability
* `05_ENVIRONMENT_VARIABLES.md` — Configuration
* `06_KNOWN_GOTCHAS.md` — Known issues
* `07_FLASHRANK_RERANKING.md` — Reranking
* `08_GUARDRAILS.md` — Guardrails
* `09_LLM_GATEWAY.md` — LLM gateway
* `10_EVALS.md` — Evaluation
* `11_EVALS_PIPELINE.md` — Evaluation pipeline

Architecture overview:

```text
ARCHITECTURE.md
```

---

# Development

Run the backend:

```bash
uvicorn app.main:app --reload
```

Run the UI:

```bash
python -m streamlit run streamlit_app.py
```

Run evaluations using the evaluation scripts under:

```text
evals/
```

---

# Repository

GitHub:

[https://github.com/ImCharli/velloehack](https://github.com/ImCharli/velloehack)

---

# Disclaimer

This software is an engineering demonstration of an enterprise RAG architecture.

The healthcare data included in this repository is intended for demonstration and evaluation purposes. The system is not a substitute for professional medical judgment and should not be used as an autonomous clinical decision-making system.

````

### One correction before you paste it

Your current project uses **Gemini in the planner/responder path**, while earlier you were also configuring Groq/Portkey. Don't claim a specific provider as the sole production LLM unless your final code actually uses it consistently.

So in the README above I deliberately wrote:

> **LLM Provider | Groq / configurable providers**

rather than claiming "Gemini" as the architecture's definitive provider.

Also, after replacing `README.md`, run:

```bash
git add README.md
git commit -m "docs: improve project README"
git push
````


