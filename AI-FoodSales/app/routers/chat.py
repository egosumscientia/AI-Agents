import os
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.catalog import find_product_from_message, get_product_row
from app.core.responses import generate_response
from app.core.summary import build_summary
from app.core.nlp_rules import detect_purchase_intent  # 🧠 Detección de intención

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

        # 🔍 Detección de producto
        canonical_name = find_product_from_message(user_input)
        print(f"[DEBUG] Producto detectado: {canonical_name}")

        # 📦 Obtener fila del catálogo
        product_row = get_product_row(canonical_name) if canonical_name else None
        print(f"[DEBUG] Fila encontrada: {product_row}")

        # 🧠 Detección de intención de compra
        intent_level = detect_purchase_intent(user_input)
        print(f"[DEBUG] Nivel de intención detectado: {intent_level}")

        # 🤖 Generar respuesta principal
        response = generate_response(product_row, user_input)

        # 🧩 Mejora en el caso de producto no encontrado (respuesta más natural)
        if not product_row:
            response["agent_response"] = (
                "No encontré ese producto en nuestro catálogo actual. "
                "¿Quieres que lo confirme un asesor o te muestro opciones similares?"
            )
            response["should_escalate"] = False

        print(f"[DEBUG] Respuesta generada: {response}")

        # 🗣️ Ajustar respuesta según intención
        if intent_level == "high":
            response["agent_response"] += (
                "\nParece que estás listo para una cotización. ¿Deseas que la gestione ahora?"
            )
        elif intent_level == "medium":
            response["agent_response"] += (
                "\nPuedo darte un valor estimado o gestionar una cotización formal. ¿Qué prefieres?"
            )

        # 📋 Crear resumen final
        summary = build_summary(user_input, response["agent_response"])
        print(f"[DEBUG] Resumen: {summary}")

        return {
            "agent_response": response["agent_response"],
            "should_escalate": response["should_escalate"],
            "summary": summary,
        }

    except Exception as e:
        import traceback
        print("[ERROR] chat_endpoint:", e)
        traceback.print_exc()
        return {
            "agent_response": "Ocurrió un error interno en el servidor.",
            "should_escalate": True,
            "summary": {"error": str(e)},
        }
