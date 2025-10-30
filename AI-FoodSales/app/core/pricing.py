
def calculate_total(product, cantidad):
    # Limpieza de claves y uniformización
    clean_product = {k.strip().lower(): v for k, v in product.items()}

    # Extrae información relevante del producto
    nombre = clean_product.get("nombre", "Producto sin nombre")
    formato = clean_product.get("formato", "")
    
    try:
        precio = float(clean_product.get("precio_lista", 0))
    except ValueError:
        precio = 0.0

    # Cálculo
    subtotal = precio * cantidad

    # Formato de respuesta
    return (
        f"{cantidad} × {nombre} ({formato}) = ${subtotal:,.0f} COP\n"
        f"Total estimado: ${subtotal:,.0f} COP (sujeto a confirmación de ventas)"
    )
