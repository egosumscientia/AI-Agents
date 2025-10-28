import os
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.catalog import find_product_from_message, get_product_row
from app.core.responses import generate_response
from app.core.summary import build_summary

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatMessage(BaseModel):
    message: str
    session_id: str | None = None
    channel: str | None = None

@router.post("/")
async def chat_endpoint(data: ChatMessage):
    try:
        print("[DEBUG] chat.py ejecutado correctamente")
        user_input = data.message.lower().strip()
        print(f"[DEBUG] Mensaje recibido: {user_input}")

        canonical_name = find_product_from_message(user_input)
        print(f"[DEBUG] Producto detectado: {canonical_name}")

        product_row = get_product_row(canonical_name) if canonical_name else None
        print(f"[DEBUG] Fila encontrada: {product_row}")

        response = generate_response(product_row, user_input)
        print(f"[DEBUG] Respuesta generada: {response}")

        summary = build_summary(user_input, response["agent_response"])
        print(f"[DEBUG] Resumen: {summary}")

        return {
            "agent_response": response["agent_response"],
            "should_escalate": response["should_escalate"],
            "summary": summary
        }

    except Exception as e:
        import traceback
        print("[ERROR] chat_endpoint:", e)
        traceback.print_exc()
        return {
            "agent_response": "Ocurrió un error interno en el servidor.",
            "should_escalate": True,
            "summary": {"error": str(e)}
        }
