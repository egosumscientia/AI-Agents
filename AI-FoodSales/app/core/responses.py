"""
Módulo de generación de respuestas AI-FoodSales
Versión: v1.4.0-courtesy-intents
Autor: Paulo & GPT-5 Lab
Descripción:
  - Prioridad total a reclamos (escalamiento antes que FAQ o logística)
  - Bloque de cortesía para saludos, agradecimientos y cierres naturales
  - Flujo semántico ordenado: cortesía → escalation → devolución → descuentos → FAQ → logística → productos
  - 100 % compatible con formato JSON y manejo de multiproducto
"""

from app.core.summary import build_summary
from app.core.escalation import should_escalate


# --- BLOQUE NUEVO: Cortesía Contextual ---
courtesy_keywords = [
    "hola", "buenos días", "buenas tardes", "buenas noches",
    "gracias", "muy amable", "te agradezco", "muchas gracias",
    "listo", "perfecto", "de acuerdo", "vale", "ok", "entendido"
]


def detect_courtesy_intent(message: str) -> bool:
    """Detecta saludos o expresiones de cortesía para evitar fallback innecesario."""
    message_lower = message.lower()
    return any(kw in message_lower for kw in courtesy_keywords)


def generate_courtesy_response(message: str) -> dict:
    """Genera respuestas empáticas para cierres o saludos."""
    lower = message.lower()
    if any(greet in lower for greet in ["hola", "buenos días", "buenas tardes", "buenas noches"]):
        text = "¡Hola! 😊 ¿En qué puedo ayudarte hoy?"
    elif any(thanks in lower for thanks in ["gracias", "muy amable", "te agradezco", "muchas gracias"]):
        text = "¡Con gusto! Si necesitas algo más, estoy aquí para ayudarte. 🙌"
    elif any(close in lower for close in ["listo", "perfecto", "de acuerdo", "vale", "ok", "entendido"]):
        text = "Excelente 👍. Quedo atento por si deseas continuar con tu pedido o consulta."
    else:
        text = "Estoy aquí si necesitas más información. 😊"

    return {
        "agent_response": text,
        "should_escalate": False,
        "summary": build_summary(message, text),
    }
# --- FIN BLOQUE NUEVO ---


def generate_response(product_data: dict, message: str):
    """
    Genera la respuesta del agente de ventas.
    """

    if not message or not isinstance(message, str):
        return {
            "agent_response": "No entendí tu mensaje. ¿Podrías reformularlo?",
            "should_escalate": False,
            "summary": build_summary(message, "Entrada inválida o vacía."),
        }

    msg = message.lower().strip()
    should_escalate_flag = False
    response_text = ""

    # 💬 1️⃣ Priorizar cortesía natural (saludos, agradecimientos, cierres)
    if detect_courtesy_intent(msg):
        return generate_courtesy_response(msg)

    # 🚨 2️⃣ Reclamos y errores (escalamiento)
    if should_escalate(msg):
        return {
            "agent_response": (
                "Entendido, escalaré tu caso para que un asesor te contacte y revise tu solicitud. "
                "Un representante verificará el pedido o la facturación en breve."
            ),
            "should_escalate": True,
            "summary": build_summary(message, "Caso escalado por reclamo logístico o financiero."),
        }

    # 💔 3️⃣ Bloque empático: producto dañado, mal olor, vencido
    if any(term in msg for term in ["dañado", "mal olor", "defectuoso", "vencido", "en mal estado"]):
        return {
            "agent_response": (
                "Lamentamos el inconveniente. Si un producto llegó dañado o en mal estado, "
                "puedes solicitar una devolución o cambio dentro de las 48 horas siguientes. "
                "¿Deseas que te envíe las instrucciones?"
            ),
            "should_escalate": False,
            "summary": build_summary(message, "Caso tratado como devolución por defecto de producto."),
        }

    # 🧠 4️⃣ Intenciones adicionales (descuentos, FAQ, etc.)
    from app.core.nlp_rules import detect_additional_intents
    intents = detect_additional_intents(message)
    if intents["should_escalate"]:
        should_escalate_flag = True

    if intents["discount_info"]:
        response_text = build_discount_response(message)
        return {
            "agent_response": response_text,
            "should_escalate": should_escalate_flag,
            "summary": build_summary(message, response_text),
        }

    if intents["faq"]:
        response_text = (
            "Pedidos mínimos: 4 unidades (Congelados), 5 (Lácteos), 12 (Bebidas) o $200.000 COP mixto.\n"
            "Tiempos de entrega: 2–3 días hábiles principales / 4–6 regionales.\n"
            "Formas de pago: transferencia, tarjeta o contraentrega (zonas urbanas).\n"
            "Devoluciones: máximo 24h con evidencia.\n"
            "¿Quieres que te gestione una cotización o más información?"
        )
        return {
            "agent_response": response_text,
            "should_escalate": should_escalate_flag,
            "summary": build_summary(message, response_text),
        }

    # 🚚 5️⃣ Logística
    from app.core.nlp_rules import detect_logistics_intent
    logistic_detected, logistic_data = detect_logistics_intent(message)
    if logistic_detected:
        subtype = logistic_data.get("type")
        city = logistic_data.get("city")
        response_text = build_logistics_response(subtype, city)
        return {
            "agent_response": response_text,
            "should_escalate": should_escalate_flag,
            "summary": build_summary(message, response_text),
        }

    # 📦 6️⃣ Productos (soporte multiproducto)
    if product_data:
        productos = []
        if isinstance(product_data, list):
            for p in product_data:
                nombre = p.get("nombre", "Producto sin nombre")
                categoria = p.get("categoria", "general")
                productos.append(f"- {nombre} ({categoria})")
        else:
            nombre = product_data.get("nombre", "Producto sin nombre")
            categoria = product_data.get("categoria", "general")
            productos.append(f"- {nombre} ({categoria})")

        joined = "\n".join(productos)
        response_text = (
            f"Tenemos disponibles los siguientes productos:\n{joined}\n"
            "¿Deseas que te envíe la cotización detallada?"
        )
    else:
        response_text = "No pude identificar el producto en tu mensaje. ¿Podrías darme más detalles?"

    return {
        "agent_response": response_text,
        "should_escalate": should_escalate_flag,
        "summary": build_summary(message, response_text),
    }


def build_logistics_response(subtype: str, city: str | None = None) -> str:
    city_delivery_map = {
        "bogota": "Para Bogotá: entrega en 2–3 días hábiles.",
        "medellin": "Para Medellín: entrega en 2–3 días hábiles.",
        "cali": "Para Cali: entrega en 3–4 días hábiles.",
        "barranquilla": "Para Barranquilla: entrega en 3–5 días hábiles.",
        "cartagena": "Para Cartagena: entrega en 3–5 días hábiles.",
        "bucaramanga": "Para Bucaramanga: entrega en 3–5 días hábiles.",
        "pereira": "Para Pereira: entrega en 3–4 días hábiles.",
        "manizales": "Para Manizales: entrega en 3–4 días hábiles.",
        "cucuta": "Para Cúcuta (zona regional): entrega en 4–6 días hábiles.",
    }

    if subtype == "weekend":
        return (
            "Realizamos entregas de lunes a sábado. "
            "Los domingos están sujetos a disponibilidad del operador logístico. "
            "¿Deseas que te confirme si tu zona tiene cobertura en fin de semana?"
        )
    elif subtype == "time_window":
        return (
            "Nuestros repartos se programan por franjas horarias: "
            "mañana (8–12), tarde (12–17) y noche (17–20), según cobertura. "
            "¿Deseas que te confirme la franja disponible para tu zona?"
        )
    elif subtype == "coverage":
        return (
            "Realizamos envíos a nivel nacional. Cobertura directa en ciudades principales "
            "y vía transportadora para zonas regionales. ¿Deseas que valide si llegamos a tu municipio?"
        )
    elif subtype == "city_delivery":
        if city:
            key = city.lower()
            city_text = city_delivery_map.get(key, "")
            return (city_text + " ¿Deseas que te confirme el tiempo exacto de entrega en esa zona?").strip()
    return (
        "Los tiempos de entrega son de 2 a 3 días hábiles en ciudades principales "
        "y de 4 a 6 días en regionales. ¿Deseas que te confirme la disponibilidad para tu zona?"
    )


def build_discount_response(message: str) -> str:
    msg = message.lower()
    if any(k in msg for k in ["bebida", "jugos", "agua", "gaseosa"]):
        return "Actualmente tenemos 10% de descuento en bebidas y jugos seleccionados."
    elif any(k in msg for k in ["lácteo", "queso", "yogurt", "leche"]):
        return "Tenemos 8% de descuento en lácteos esta semana."
    elif any(k in msg for k in ["congelado", "carne", "pollo", "pescado"]):
        return "Promoción del 12% en congelados hasta el domingo."
    else:
        return "Tenemos promociones activas en varias categorías. ¿Te gustaría conocer las ofertas actuales?"
