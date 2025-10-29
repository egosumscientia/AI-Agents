from app.core.summary import build_summary

def generate_response(product_data: dict, message: str):
    """
    Genera la respuesta del agente de ventas según el mensaje del usuario.
    Ahora incluye detección de FAQs y escalamiento automático.
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

    # 🚚 Detección avanzada de logística (antes del FAQ)
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

    # 🔒 Escalamiento automático
    if any(word in msg for word in ["certificado", "invima", "contrato", "reclamo", "negociar"]):
        should_escalate = True

    # 📦 Preguntas frecuentes (FAQ)
    if any(word in msg for word in ["mínimo", "minimos", "entrega", "pago", "pagos", "devolución", "envío", "envios", "tiempo de entrega"]):
        response_text = (
            "Los pedidos mínimos son: 4 unidades (Congelados), 5 (Lácteos), 12 (Bebidas) o $200.000 COP mixto.\n"
            "Tiempos de entrega: 2–3 días hábiles en ciudades principales, 4–6 días en regionales.\n"
            "Formas de pago: transferencia, tarjeta o contraentrega en clientes urbanos recurrentes.\n"
            "Devoluciones: máximo 24h con evidencia.\n"
            "¿Quieres que te gestione una cotización o información más detallada?"
        )
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
    Ampliada para manejar subtipos:
      - generic
      - weekend
      - coverage
      - city_delivery
      - time_window
    Además personaliza por ciudad cuando aplica.
    """

    # --- Base de mensajes por ciudad ---
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

    # --- Mensajes base por subtipo ---
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
        base_text = (
            (city_text + " ") if city_text else ""
        ) + "¿Deseas que te confirme el tiempo exacto de entrega en esa zona?"

    else:  # generic y fallback
        base_text = (
            "Los tiempos de entrega son de 2 a 3 días hábiles en ciudades principales "
            "y de 4 a 6 días en regionales. ¿Deseas que te confirme la disponibilidad para tu zona?"
        )

    return base_text
