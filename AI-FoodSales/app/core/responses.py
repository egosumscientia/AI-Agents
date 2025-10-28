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

# === NUEVO BLOQUE: respuesta logística específica ===
def build_logistics_response(subtype: str, city: str | None = None) -> str:
    """
    Genera una respuesta específica de logística sin interferir con el bloque FAQ.
    """
    if subtype == "weekend":
        base_text = (
            "Realizamos despachos de lunes a viernes. "
            "Sábados sujetos a cobertura del operador logístico. "
            "Los tiempos de entrega son de 2 a 3 días hábiles en ciudades principales "
            "y de 4 a 6 días en regionales. ¿Deseas que te confirme la disponibilidad para tu zona?"
        )
    else:
        base_text = (
            "Los tiempos de entrega son de 2 a 3 días hábiles en ciudades principales "
            "y de 4 a 6 días en regionales. ¿Deseas que te confirme la disponibilidad para tu zona?"
        )

    if city:
        base_text = f"Para {city}: {base_text}"

    return base_text
