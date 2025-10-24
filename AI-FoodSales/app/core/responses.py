def generate_response(product):
    if not product:
        return "Ese producto no está en el catálogo cargado. ¿Quieres que lo confirme un asesor?"
    return (f"Tenemos disponible el {product['Producto']} en presentación {product['Formato']}."
            f"\nPrecio estimado: ${product['Precio']} COP/unidad."
            f"\nPedido mínimo: {product['Minimo']} unidades."
            "\n¿Quieres que te gestione la cotización?")

def faq_response(topic):
    faq = {
        "mínimo": "Congelados: 4 unidades, Lácteos: 5, Bebidas: 12, Mixto: $200.000 COP mínimo.",
        "pago": "Transferencia, tarjeta, contraentrega (clientes urbanos), crédito a 30 días con aprobación.",
        "entrega": "2–3 días en ciudades principales, 4–6 días regionales, 7 días para grandes volúmenes.",
        "invima": "Sí, todos los productos tienen certificado INVIMA."
    }
    for key, answer in faq.items():
        if key in topic:
            return answer
    return "Puedo revisar eso con un asesor si deseas una respuesta detallada."
