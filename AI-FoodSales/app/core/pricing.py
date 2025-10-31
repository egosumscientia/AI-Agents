import re

def calculate_total(product, cantidad):
    clean_product = {k.strip().lower(): v for k, v in product.items()}
    nombre  = clean_product.get("nombre", "Producto sin nombre")
    formato = clean_product.get("formato", "")
    info_descuento = str(clean_product.get("descuento_mayorista_volumen", "")).strip()
    print(f"[TRACE] info_descuento -> '{info_descuento}'", flush=True)

    try:
        precio = float(str(clean_product.get("precio_lista", 0)).replace(",", "."))
    except ValueError:
        precio = 0.0

    # --------------------- DESCUENTO POR VOLUMEN ---------------------
    # Extrae el número justo antes del símbolo %, ignorando todo lo anterior
    porcentaje = 0.0
    umbral = 0

    # Busca el número que precede directamente al '%'
    m_desc = re.search(r"(\d+(?:[.,]\d+)?)\s*%\s*a partir de\s+(\d+)\s+unidades", info_descuento)
    if m_desc:
        porcentaje_txt = m_desc.group(1).replace(",", ".")
        try:
            porcentaje = float(porcentaje_txt)
        except ValueError:
            porcentaje = 0.0
        umbral = int(m_desc.group(2))

    # --------------------- CÁLCULO ---------------------
    subtotal = precio * cantidad

    if porcentaje > 0 and umbral > 0 and cantidad >= umbral:
        descuento_valor = subtotal * (porcentaje / 100.0)
        total = subtotal - descuento_valor
        return (
            f"{cantidad} × {nombre} ({formato}) = ${subtotal:,.0f} COP\n"
            f"Descuento aplicado: {porcentaje:.1f}% (-${descuento_valor:,.0f})\n"
            f"Total: ${total:,.0f} COP"
        )
    else:
        return (
            f"{cantidad} × {nombre} ({formato}) = ${subtotal:,.0f} COP\n"
            f"Total: ${subtotal:,.0f} COP"
        )
