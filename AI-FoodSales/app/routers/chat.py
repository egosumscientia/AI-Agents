from fastapi import APIRouter
from pydantic import BaseModel
from app.core.nlp_rules import detect_intent, normalize_input
from app.core.catalog import find_product
from app.core.responses import generate_response, faq_response
from app.core.escalation import should_escalate
from app.core.summary import build_summary
from app.utils.logger import log_interaction

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatMessage(BaseModel):
    message: str
    session_id: str | None = None
    channel: str | None = None

@router.post("/")
async def chat_endpoint(data: ChatMessage):
    user_input = data.message.lower().strip()
    intent = detect_intent(user_input)
    normalized = normalize_input(user_input)

    if intent == "quote":
        product = find_product(normalized)
        response = generate_response(product)
    elif intent == "faq":
        response = faq_response(normalized)
    else:
        response = "¿Podrías especificar qué producto o información necesitas?"

    escalation = should_escalate(user_input)
    summary = build_summary(user_input, response)
    log_interaction(data.session_id or "default", user_input, response, data.channel or "unknown")

    return {"agent_response": response, "should_escalate": escalation, "summary": summary}
