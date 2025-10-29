# app/core/nlp_rules.py
import json, os, re
from difflib import SequenceMatcher

DATA_DIR = os.path.join('app', 'data')
SYNONYMS_FILE = os.path.join(DATA_DIR, 'synonyms.json')


# -------------------------------------------------------------
# INTENCIÓN GENERAL
# -------------------------------------------------------------
def detect_intent(text: str) -> str:
    text = text.lower()
    if any(k in text for k in ['precio', 'cuánto', 'cotiza', 'total', 'cuenta']):
        return 'quote'
    if any(k in text for k in ['tiempo', 'entrega', 'mínimo', 'pago', 'invima', 'certificado']):
        return 'faq'
    return 'other'


# -------------------------------------------------------------
# INTENCIÓN DE COMPRA
# -------------------------------------------------------------
def detect_purchase_intent(text: str) -> str:
    text = text.lower()

    high_intent = [
        "envíame", "hazme la cuenta", "quiero pedir", "cotízame",
        "necesito para", "urgente", "mándame la cotización",
        "cómo te pago", "cuánto me sale", "ya tengo pedido"
    ]

    medium_intent = [
        "me interesa", "cuánto vale", "qué precio tiene",
        "pueden enviar", "cuánto demora", "quiero saber si tienen",
        "podrían cotizarme", "estoy mirando precios"
    ]

    if any(p in text for p in high_intent):
        return "high"
    elif any(p in text for p in medium_intent):
        intent = "medium"
    else:
        intent = "low"

    # Detección de pedidos grandes
    if re.search(r'(\b\d+\s*(unidades?|cajas?|bultos?|litros?|kilos?|sacos?)\b|\bpedido grande\b|\ben cantidad\b)', text):
        return "high"

    return intent


# -------------------------------------------------------------
# INTENCIÓN LOGÍSTICA
# -------------------------------------------------------------
def detect_logistics_intent(text: str) -> tuple[bool, dict]:
    """
    Detecta si el mensaje se refiere a temas logísticos (entrega, cobertura, etc.).
    Retorna (True/False, {"type": str, "city": Optional[str]}).
    """
    if not text:
        return False, {}

    import unicodedata

    text = text.lower().strip()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.replace("¿", "").replace("?", "").replace("¡", "").replace("!", "")

    logistics_keywords = [
        r"\b(entrega|entregan|entregar|entregado|entregas)\b",
        r"\b(envio|envian|enviar|enviarlo|envios)\b",
        r"\b(despacho|despachos|despachan|despachar)\b",
        r"\b(reparto|repartos|domicilio|domicilios|mensajeria|repartidor)\b",
        r"\b(cobertura|cubren|alcance)\b",
        r"\b(horario|hora|horas|mañana|tarde|noche|noches|fines?\s+de\s+semana|sabados?|domingos?)\b"
    ]

    if not any(re.search(pat, text) for pat in logistics_keywords):
        return False, {}

    # Tipificación logística
    if re.search(r"\b(fines?\s+de\s+semana|sabados?|domingos?)\b", text):
        subtype = "weekend"
    elif re.search(r"\b(horario|hora|horas|mañana|tarde|noche|noches)\b", text):
        subtype = "time_window"
    elif re.search(r"\b(cobertura|cubren|alcance|otras?\s+ciudades|fuera|nacional|envian\s+a)\b", text):
        subtype = "coverage"
    elif re.search(r"\b(cuanto\s+tardan?|tiempos?\s+de\s+entrega|plazo)\b", text):
        subtype = "delivery_time"
    else:
        subtype = "generic"

    city_match = re.search(
        r"\b(en|a)\s+(bogota|medellin|cali|barranquilla|cartagena|bucaramanga|pereira|manizales|cucuta)\b",
        text,
    )
    city = city_match.group(2).title() if city_match else None
    if city and subtype == "generic":
        subtype = "city_delivery"

    return True, {"type": subtype, "city": city}


# -------------------------------------------------------------
# NORMALIZACIÓN MULTIPRODUCTO
# -------------------------------------------------------------
def normalize_input(text: str) -> list[str]:
    """
    Busca todos los productos mencionados en el texto.
    Devuelve lista con nombres canónicos encontrados.
    """
    try:
        with open(SYNONYMS_FILE, encoding='utf-8') as f:
            synonyms = json.load(f)
    except Exception:
        synonyms = {}

    msg = text.lower().strip()
    encontrados = set()

    for canonical, variants in synonyms.items():
        for v in variants:
            term = v.lower().strip()
            if term in msg:
                encontrados.add(canonical)
            elif any(w in msg.split() or w in msg for w in term.split()):
                encontrados.add(canonical)
            elif SequenceMatcher(None, term, msg).ratio() > 0.7:
                encontrados.add(canonical)

    return list(encontrados)


# -------------------------------------------------------------
# INTENCIONES ADICIONALES
# -------------------------------------------------------------
def detect_additional_intents(text: str) -> dict:
    """
    Detecta intenciones adicionales: FAQ, discount_info, should_escalate.
    Prioridad: should_escalate > logistics > faq > discount.
    """
    text = text.lower()
    intents = {"faq": False, "discount_info": False, "should_escalate": False}

    faq_keywords = [
        "mínimo", "minimos", "compra mínima", "pedido mínimo",
        "forma de pago", "formas de pago", "pago", "pagos",
        "contraentrega", "efectivo", "tarjeta", "crédito", "débito",
        "devolución", "devoluciones", "cambio", "cambios",
        "reembolso", "reembolsos", "tiempo de entrega", "entregan",
        "cuánto se demora la entrega", "disponibilidad", "stock", "existencias",
        "dañado", "mal olor", "defectuoso", "combinar", "mezclar", "mismo pedido"
    ]
    if any(k in text for k in faq_keywords):
        intents["faq"] = True

    discount_keywords = [
        "promocion", "promoción", "oferta", "descuento", "descuentos",
        "rebaja", "promo", "en oferta"
    ]
    if any(k in text for k in discount_keywords):
        intents["discount_info"] = True

    escalate_keywords = [
        "reclamo", "problema", "queja", "certificado adicional",
        "certificado invima", "documento adicional", "error", "equivocado",
        "mal", "confusión", "pedido incorrecto", "producto equivocado",
        "pedido incompleto", "demora", "retraso", "no ha llegado", "todavía no llega",
        "repartidor", "cobrado", "cobro incorrecto", "precio distinto"
    ]
    if any(k in text for k in escalate_keywords):
        intents["should_escalate"] = True

    # Prioridad semántica: si hay escalamiento → anula todo lo demás
    if intents["should_escalate"]:
        intents["faq"] = False
        intents["discount_info"] = False

    return intents
