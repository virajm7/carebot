from fastapi import APIRouter
from app.models.schema import Query, Answer
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService

router = APIRouter()

rag = RAGService()
llm = LLMService()

SYSTEM_PROMPT = """
You are an information assistant for Dr. Pooja’s Rehab & Therapy Clinic.
You must answer ONLY using the information from the provided context.
Do not invent facts, do not guess, do not use outside knowledge.
Rewrite the retrieved information in a clear, polite, professional tone.
If the information is not found in the clinic knowledge base, respond with:
"I'm sorry, but that information is not available in the clinic’s knowledge records."
"""

@router.post("/ask", response_model=Answer)
def ask_bot(body: Query):
    user_query = body.query

    # retrieve
    context = rag.search(user_query)

    if context is None:
        return {"response": "I'm sorry, but that information is not available in the clinic’s knowledge records."}

    # generate human-like answer
    reply = llm.ask(SYSTEM_PROMPT, context, user_query)

    return {"response": reply}
