import os
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.catalog import find_product_from_message, get_product_row
from app.core.responses import generate_response, build_logistics_response
from app.core.summary import build_summary
from app.core.nlp_rules import detect_purchase_intent, detect_logistics_intent

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatMessage(BaseModel):
    message: str
    session_id: str | None = None
    channel: str | None = None


@router.post("/")
async def chat_endpoint(data: ChatMessage):
    try:
        user_input = data.message.lower().strip()

        # 🔍 Detección de producto
        canonical_name = find_product_from_message(user_input)
        product_row = get_product_row(canonical_name) if canonical_name else None

        # 🧠 Detección de intención de compra
        intent_level = detect_purchase_intent(user_input)

        # 🤖 Generar respuesta principal
        response = generate_response(product_row, user_input)

        # 🧠 Asegurar que detect_additional_intents se evalúe antes de logística
        from app.core.nlp_rules import detect_additional_intents
        intents = detect_additional_intents(user_input)

        # Priorizar reclamos o certificados sobre logística
        if intents.get("should_escalate"):
            response["should_escalate"] = True


        # 🚚 Detección de intención logística (solo si no hay reclamo ni descuento)
        logistic_detected, logistic_info = (False, {})
        if not intents.get("should_escalate") and not intents.get("discount_info"):
            logistic_detected, logistic_info = detect_logistics_intent(user_input)

        if logistic_detected and "entrega" not in response["agent_response"]:
            subtype = logistic_info.get("type")
            city = logistic_info.get("city")
            logistics_text = build_logistics_response(subtype, city)

            # Si hay producto → combinar ambas respuestas
            if product_row:
                response["agent_response"] += f"\n\n{logistics_text}"
            else:
                # Solo logística (sin producto)
                return {
                    "agent_response": logistics_text,
                    "should_escalate": False,
                    "summary": {
                        "pedido_o_consulta": user_input,
                        "accion_del_agente": "Información logística entregada.",
                        "intencion_compra": intent_level,
                        "delivery_info": {
                            "detected": True,
                            "type": subtype,
                            "city": city,
                        },
                    },
                }

        # 🧩 Caso: producto no encontrado y sin intención logística
        # Mantener respuesta previa (FAQ o descuento), pero usar fallback solo si no hubo respuesta generada.
        if not product_row and not logistic_detected and not response.get("agent_response"):
            response["agent_response"] = (
                "No encontré ese producto en nuestro catálogo actual. "
                "¿Quieres que lo confirme un asesor o te muestro opciones similares?"
            )
            response["should_escalate"] = response.get("should_escalate", False)


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
