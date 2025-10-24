def calculate_total(product, cantidad):
    precio = float(product.get("Precio", 0))
    subtotal = precio * cantidad
    total = subtotal
    return f"{cantidad} x {product['Producto']} ({product['Formato']}) = ${subtotal:,.0f} COP\nTotal estimado: ${total:,.0f} COP (sujeto a confirmación de ventas)"
