"""
Módulo de detección de escalamiento inteligente
Versión: v1.3.10-smart-escalation
Autor: Paulo & GPT-5 Lab
Descripción:
    Detección refinada de reclamos logísticos, financieros y de pedidos incompletos.
    Cobertura semántica ampliada para variaciones naturales del lenguaje.
"""

def should_escalate(text: str) -> bool:
    """
    Determina si el texto requiere escalar a atención humana.
    Retorna True si se detecta un reclamo, error o incidencia.
    """

    if not text:
        return False

    text = text.lower().strip()

    escalation_keywords = [
        # Reclamos y problemas generales
        "reclamo", "problema", "queja", "error", "equivocado", "mal", "malo",
        "defectuoso", "descompuesto", "deteriorado", "confusión", "confundí", "en mal estado",
        "no entiendo", "no corresponde", "dañado", "inservible", "roto", "podrido", "vencido", "quebrado",
        "incompleto", "faltantes", "menos productos", "menos de lo solicitado", "precio diferente",
        "precio distinto", "factura diferente",

        # Pedidos y entregas con error
        "pedido incorrecto", "producto equivocado", "me llegó mal",
        "no ha llegado", "no llego", "no me llegó", "no me ha llegado",
        "vino incompleto", "llegó incompleto", "entregaron incompleto",
        "pedido incompleto", "entrega incompleta",
        "faltante", "faltó", "faltaron", "no completo", "menos de lo pedido",
        "demora", "retraso", "tarde", "no aparece", "todavía no llega",
        "entrega pendiente", "repartidor", "no pudo entregar", "no puede entregar",
        "pedido vino incompleto", "vino incompleto", "vino mal", "vino con faltantes",
        "pedido vino mal despachado", "pedido vino defectuoso",
        "despacho", "mal despachado", "error de despacho",

        # Casos administrativos o de soporte documental
        "contrato", "certificado adicional", "certificado invima",
        "documento adicional", "invima", "soporte adicional",

        # Casos financieros o de cobro
        "cobrado", "me cobraron", "cobraron", "cobrar", "cobro incorrecto",
        "precio distinto", "error en factura", "cobro duplicado",
        "error en cobro", "factura mal", "valor diferente", "costo equivocado",
        "precio errado", "precio equivocado", "precio incorrecto",
        "sobreprecio", "sobre cobro", "me cobraron de más",
    ]

    return any(k in text for k in escalation_keywords)
