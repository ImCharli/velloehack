import logfire
from app.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agents.state import AgentState


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0,
    google_api_key=settings.GEMINI_API_KEY,
)


def planner_node(state: AgentState):
    """
    Determines whether the query is conversational or requires
    enterprise knowledge retrieval.
    """

    history = ""

    for msg in state["messages"][:-1]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"

    user_message = (
        state["messages"][-1]["content"]
        if state["messages"]
        else ""
    )

    prompt = f"""
You are an Enterprise RAG Planner.

CONVERSATION HISTORY:
{history}

LATEST USER MESSAGE:
{user_message}

Determine whether the user needs enterprise document retrieval.

Rules:

1. If the message is a greeting, casual conversation, or can be answered
   entirely from the conversation history, output exactly:

CONVERSATIONAL

2. If the user asks about company documentation, policies, SOPs,
   guidelines, procedures, formulary information, devices, healthcare
   documents, or any factual information that should come from the
   enterprise knowledge base, output a concise search query.

3. Never answer the user's question yourself.

Output ONLY:
- CONVERSATIONAL
OR
- a refined search query
"""

    with logfire.span("🧠 Planner Decision"):
        response = llm.invoke(prompt)

        content = response.content

        if isinstance(content, list):
            decision = "".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict)
            ).strip()
        else:
            decision = str(content).strip()

        logfire.info(f"Intent identified: {decision}")

    if decision.upper() == "CONVERSATIONAL":
        return {
            "current_query": "CONVERSATIONAL",
            "status": "Handling conversationally (using memory)...",
            "plan": [
                "Intent: Conversational/Memory",
                "Retrieval: Skipped",
            ],
        }

    return {
        "current_query": decision,
        "status": f"Technical research needed. Searching for: {decision}",
        "plan": [
            "Intent: Enterprise Knowledge",
            f"Search Term: {decision}",
        ],
    }