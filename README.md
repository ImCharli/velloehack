# Velloe Enterprise AI

A production-oriented enterprise healthcare knowledge assistant built using
**FastAPI, LangGraph, Qdrant, Gemini, NeMo Guardrails, reranking, and Streamlit**.

The system retrieves relevant enterprise knowledge, reranks the retrieved
documents, and generates grounded answers using the retrieved context.

---

## Architecture

```text
                         ┌──────────────────────┐
                         │     Streamlit UI     │
                         │  Healthcare Assistant│
                         └──────────┬───────────┘
                                    │
                              POST /query
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │      API Layer       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   LangGraph Agent    │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         │                      │
                         ▼                      ▼
                ┌─────────────────┐    ┌─────────────────┐
                │     Planner     │    │   Conversation  │
                │ Intent + Query  │    │     Memory      │
                └────────┬────────┘    └─────────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Qdrant       │
                │ Vector Search   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Reranker     │
                │   FlashRank     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     Gemini      │
                │ Answer Synthesis│
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Grounded Answer │
                │ + Evidence      │
                └─────────────────┘