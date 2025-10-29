from app.core.summary import build_summary

def generate_response(product_data: dict, message: str):
    """
    Genera la respuesta del agente de ventas según el mensaje del usuario.
    Versión v1.3.1-faq-discount
    Incluye:
      - Ampliación de FAQs
      - Nueva intención discount_info
      - Escalamiento automático
      - Mantiene compatibilidad logística
    """

    if not message or not isinstance(message, str):
        return {
            "agent_response": "No entendí tu mensaje. ¿Podrías reformularlo?",
            "should_escalate": False,
            "summary": build_summary(message, "Entrada inválida o vacía.")
        }

    msg = message.lower()
    should_escalate = False
    response_text = ""

    # ⚠️ Priorizar reclamos o certificados sobre cualquier otra intención
    if any(word in msg for word in ["reclamo", "problema", "queja", "certificado adicional", "invima"]):
        return {
            "agent_response": "Entendido, escalaré este caso para que un asesor te contacte y revise tu solicitud.",
            "should_escalate": True,
            "summary": build_summary(message, "Caso marcado para revisión manual por reclamo o certificado.")
        }


    # 🧠 Intenciones adicionales (FAQ, descuentos, escalamiento)
    from app.core.nlp_rules import detect_additional_intents
    intents = detect_additional_intents(message)

    if intents["should_escalate"]:
        should_escalate = True

    # 🔸 Nueva intención: descuentos/promociones
    if intents["discount_info"]:
        from app.core.responses import build_discount_response
        response_text = build_discount_response(message)
        return {
            "agent_response": response_text,
            "should_escalate": should_escalate,
            "summary": build_summary(message, response_text)
        }

    # 🔸 FAQ ampliado
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
            "should_escalate": should_escalate,
            "summary": build_summary(message, response_text)
        }

    # 🚚 Detección avanzada de logística (después de FAQ)
    from app.core.nlp_rules import detect_logistics_intent
    logistic_detected, logistic_data = detect_logistics_intent(message)
    if logistic_detected:
        from app.core.responses import build_logistics_response
        subtype = logistic_data.get("type")
        city = logistic_data.get("city")
        response_text = build_logistics_response(subtype, city)
        return {
            "agent_response": response_text,
            "should_escalate": should_escalate,
            "summary": build_summary(message, response_text)
        }

    # 🧾 Si hay producto detectado
    if product_data:
        nombre = product_data.get("nombre", "Producto sin nombre")
        formato = product_data.get("formato", "presentación no especificada")
        precio = product_data.get("precio_lista", "sin precio")
        moneda = product_data.get("precio_lista_moneda", "COP")
        minimo = product_data.get("unidad_minima", "N/D")
        categoria = product_data.get("categoria", "general")
        descuento = product_data.get("descuento_mayorista_volumen", "sin descuento")
        comentario = product_data.get("comentarios", "")

        response_text = (
            f"Tenemos disponible el {nombre} ({categoria}).\n"
            f"Presentación: {formato}.\n"
            f"Precio estimado: ${precio} {moneda}.\n"
            f"Pedido mínimo: {minimo} unidades.\n"
            f"Descuento: {descuento}.\n"
            f"{comentario}\n¿Quieres que te gestione la cotización?"
        )
    else:
        response_text = "No pude identificar el producto en tu mensaje. ¿Podrías darme más detalles?"

    return {
        "agent_response": response_text,
        "should_escalate": should_escalate,
        "summary": build_summary(message, response_text)
    }


def build_logistics_response(subtype: str, city: str | None = None) -> str:
    """
    Genera una respuesta específica de logística sin interferir con el bloque FAQ.
    Subtipos: generic, weekend, coverage, city_delivery, time_window
    """

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
        base_text = (
            "Realizamos entregas de lunes a sábado. "
            "Los domingos están sujetos a disponibilidad del operador logístico. "
            "¿Deseas que te confirme si tu zona tiene cobertura en fin de semana?"
        )
    elif subtype == "time_window":
        base_text = (
            "Nuestros repartos se programan por franjas horarias: "
            "mañana (8–12), tarde (12–17) y noche (17–20), según cobertura. "
            "¿Deseas que te confirme la franja disponible para tu zona?"
        )
    elif subtype == "coverage":
        base_text = (
            "Realizamos envíos a nivel nacional. "
            "Cobertura directa en ciudades principales y vía transportadora para zonas regionales. "
            "Tiempos de entrega promedio: 2–3 días hábiles en ciudades principales, "
            "4–6 días en zonas regionales. "
            "¿Deseas que valide si llegamos a tu municipio?"
        )
    elif subtype == "city_delivery":
        city_text = ""
        if city:
            key = city.lower()
            city_text = city_delivery_map.get(key, "")
        base_text = ((city_text + " ") if city_text else "") + \
            "¿Deseas que te confirme el tiempo exacto de entrega en esa zona?"
    else:
        base_text = (
            "Los tiempos de entrega son de 2 a 3 días hábiles en ciudades principales "
            "y de 4 a 6 días en regionales. ¿Deseas que te confirme la disponibilidad para tu zona?"
        )

    return base_text


def build_discount_response(message: str) -> str:
    """
    Genera respuesta predefinida sobre descuentos/promociones.
    """
    msg = message.lower()
    if any(k in msg for k in ["bebida", "jugos", "agua", "gaseosa"]):
        return "Actualmente tenemos 10% de descuento en bebidas y jugos seleccionados."
    elif any(k in msg for k in ["lácteo", "queso", "yogurt", "leche"]):
        return "Tenemos 8% de descuento en lácteos esta semana."
    elif any(k in msg for k in ["congelado", "carne", "pollo", "pescado"]):
        return "Promoción del 12% en congelados hasta el domingo."
    else:
        return "Tenemos promociones activas en varias categorías. ¿Te gustaría conocer las ofertas actuales?"
