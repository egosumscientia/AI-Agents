from app.core.summary import build_summary

def generate_response(product_data: dict, message: str):
    """
    Genera la respuesta del agente usando los datos ya detectados del producto.
    """
    if not product_data:
        return {
            "agent_response": "No pude identificar el producto en tu mensaje. ¿Podrías darme más detalles?",
            "should_escalate": False,
            "summary": build_summary(message, "Consulta sin producto detectado.")
        }

    nombre = product_data.get("nombre", "Producto sin nombre")
    formato = product_data.get("formato", "presentación no especificada")
    precio = product_data.get("precio_lista", "sin precio")
    moneda = product_data.get("precio_lista_moneda", "COP")
    minimo = product_data.get("unidad_minima", "N/D")
    categoria = product_data.get("categoria", "general")
    descuento = product_data.get("descuento_mayorista_volumen", "sin descuento")
    comentario = product_data.get("comentarios", "")

    agent_response = (
        f"Tenemos disponible el {nombre} ({categoria}).\n"
        f"Presentación: {formato}.\n"
        f"Precio estimado: ${precio} {moneda}.\n"
        f"Pedido mínimo: {minimo} unidades.\n"
        f"Descuento: {descuento}.\n"
        f"{comentario}\n"
        f"¿Quieres que te gestione la cotización?"
    )

    return {
        "agent_response": agent_response,
        "should_escalate": False,
        "summary": build_summary(message, agent_response)
    }
