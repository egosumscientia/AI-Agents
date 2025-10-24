def calculate_total(product, cantidad):
    precio = float(product.get('Precio', 0) or 0)
    subtotal = precio * cantidad
    total = subtotal
    return f"{cantidad} x {product.get('Producto')} ({product.get('Formato')}) = ${subtotal:,.0f} COP\nTotal estimado: ${total:,.0f} COP (sujeto a confirmación de ventas)"
