import logfire
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agents.state import AgentState
from app.config import settings


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.1,
    google_api_key=settings.GEMINI_API_KEY,
)


def generate_node(state: AgentState):
    """
    Generates the final answer using retrieved enterprise context
    and conversation history.
    """

    query = state["current_query"]

    history_str = ""

    for msg in state["messages"][:-1]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_str += f"{role}: {msg['content']}\n"

    user_msg = (
        state["messages"][-1]["content"]
        if state["messages"]
        else ""
    )

    if query == "CONVERSATIONAL":

        prompt = f"""
You are a friendly Enterprise AI Assistant.

Answer the user's latest message using the conversation history.

CONVERSATION HISTORY:
{history_str}

LATEST USER MESSAGE:
{user_msg}
"""

    else:

        full_context = ""

        for doc in state.get("documents", []):
            full_context += doc + "\n\n"

        prompt = f"""
You are a Senior Enterprise AI Assistant.

Answer the user's question using ONLY the enterprise
documentation provided below.

IMPORTANT:
- Do not invent facts.
- If the documentation does not contain the answer, say so.
- Prefer the most specific and relevant evidence.
- For healthcare information, clearly state relevant
  conditions such as population or weight range.
- Do not provide information that is not supported by
  the retrieved enterprise documents.

ENTERPRISE DOCUMENTATION:
{full_context}

CONVERSATION HISTORY:
{history_str}

USER QUESTION:
{user_msg}
"""

    with logfire.span("✍️ LLM Synthesis"):

        try:

            response = llm.invoke(prompt)

            content = response.content

            if isinstance(content, list):
                answer = "".join(
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict)
                ).strip()
            else:
                answer = str(content).strip()

            logfire.info("✅ Response synthesised via Gemini.")

            return {
                "final_answer": answer,
                "status": "Response generated.",
                "plan": state.get("plan", []),
                "messages": [
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                ],
            }

        except Exception as e:

            logfire.error(f"LLM Generation failed: {e}")
            raise