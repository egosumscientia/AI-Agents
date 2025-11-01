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


# --- BLOQUE NUEVO: detección de cortesía ---
courtesy_keywords = [
    "hola", "buenos días", "buenas tardes", "buenas noches",
    "gracias", "muy amable", "te agradezco", "muchas gracias",
    "listo", "perfecto", "de acuerdo", "vale", "ok", "entendido"
]

def detect_courtesy_intent(message: str) -> bool:
    message_lower = message.lower()
    return any(kw in message_lower for kw in courtesy_keywords)

def generate_courtesy_response(message: str) -> str:
    lower = message.lower()
    if any(greet in lower for greet in ["hola", "buenos días", "buenas tardes", "buenas noches"]):
        return "¡Hola! 😊 ¿En qué puedo ayudarte hoy?"
    elif any(thanks in lower for thanks in ["gracias", "muy amable", "te agradezco", "muchas gracias"]):
        return "¡Con gusto! Si necesitas algo más, estoy aquí para ayudarte. 🙌"
    elif any(close in lower for close in ["listo", "perfecto", "de acuerdo", "vale", "ok", "entendido"]):
        return "Excelente 👍. Quedo atento por si deseas continuar con tu pedido o consulta."
    else:
        return "Estoy aquí si necesitas más información. 😊"
# --- FIN BLOQUE NUEVO ---


@router.post("/")
async def chat_endpoint(data: ChatMessage):
    try:
        user_input = data.message.lower().strip()

        # 💬 Detección de cortesía (solo si no hay frustración ni sarcasmo)
        if detect_courtesy_intent(user_input):
            from app.core.escalation import should_escalate
            result = should_escalate(user_input)
            if result.get("summary", {}).get("scores", {}).get("sarcasm", 0) < 0.8:
                return {
                    "agent_response": generate_courtesy_response(user_input),
                    "should_escalate": False,
                    "summary": {"tipo": "cortesía", "mensaje": user_input}
                }
            else:
                # Si hay sarcasmo o frustración, se sigue con el flujo normal
                pass

        # 🔍 Detección de producto
        canonical_name = find_product_from_message(user_input)
        product_row = get_product_row(canonical_name) if canonical_name else None

        # 🧮 Detección de múltiples productos y cantidades
        from app.core import nlp_rules, pricing

        items = nlp_rules.extract_products_and_quantities(user_input)

        if items:
            response_lines = []
            total_general = 0

            for item in items:
                prod_name = item["nombre"]
                qty = item["cantidad"]

                prod_row = get_product_row(prod_name)
                if not prod_row:
                    response_lines.append(f"No encontré '{prod_name}' en el catálogo.")
                    continue

                from app.core.pricing import calculate_total
                resultado = calculate_total(prod_row, qty)
                response_lines.append(resultado)

                import re
                match = re.search(r"Total: \$([\d,]+)", resultado)
                if match:
                    monto = int(match.group(1).replace(",", ""))
                    total_general += monto

            # ✅ total general (solo si hay productos válidos)
            if total_general > 0:
                response_lines.append(f"🟩 Total general: ${total_general:,.0f} COP")

            # 🧠 Detección de reclamos o sarcasmo antes de responder
            from app.core.escalation import should_escalate
            escalation_result = should_escalate(user_input) or {}
            
            if escalation_result.get("should_escalate"):
                print(">>> ESCALAMIENTO PRESERVADO DESDE CHAT")
                return escalation_result

            # 🔸 Respuesta final consolidada (solo si no hay reclamo)
            return {
                "agent_response": "\n".join(response_lines),
                "should_escalate": False,
                "summary": {
                    "pedido_o_consulta": user_input,
                    "accion_del_agente": f"Cálculo múltiple para {len(items)} productos",
                },
            }

        # 👇 Si no hay productos, continúa flujo general (sarcasmo, reclamos, logística, etc.)

        # 🧠 Detección de intención de compra
        intent_level = detect_purchase_intent(user_input)

        # 🤖 Generar respuesta principal
        response = generate_response(product_row, user_input)

        # --- Prioridad de respuestas informativas directas (INVIMA, IVA, etc.) ---
        if "invima" in user_input or "certificado invima" in user_input:
            return response
        
        if "iva" in user_input or "incluye iva" in user_input or "precio con iva" in user_input:
            return response

        # ✅ Preservar resultado de escalamiento si el mensaje es reclamo o sarcasmo
        from app.core.escalation import should_escalate
        escalation_result = should_escalate(user_input)
        if escalation_result.get("should_escalate"):
            print(">>> ESCALAMIENTO PRESERVADO DESDE CHAT")
            return escalation_result

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

            if product_row:
                response["agent_response"] += f"\n\n{logistics_text}"
            else:
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
            
        # ✅ failsafe añadido aquí
        response = response or {}

        # 🧩 Caso: producto no encontrado y sin intención logística
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
