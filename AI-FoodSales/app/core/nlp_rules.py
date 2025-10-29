import json, os, re
from difflib import SequenceMatcher

DATA_DIR = os.path.join('app', 'data')
SYNONYMS_FILE = os.path.join(DATA_DIR, 'synonyms.json')

def detect_intent(text: str) -> str:
    text = text.lower()
    if any(k in text for k in ['precio', 'cuánto', 'cotiza', 'total', 'cuenta']):
        return 'quote'
    if any(k in text for k in ['tiempo', 'entrega', 'mínimo', 'pago', 'invima', 'certificado']):
        return 'faq'
    return 'other'

def detect_purchase_intent(text: str) -> str:
    """
    Detecta el nivel de intención de compra ('high', 'medium', 'low')
    basado en señales contextuales del mensaje del cliente.
    """
    text = text.lower()

    # Alta intención: ya está comprando o pide acción inmediata
    high_intent = [
        "envíame", "hazme la cuenta", "quiero pedir", "cotízame", 
        "necesito para", "urgente", "mándame la cotización", 
        "cómo te pago", "cuánto me sale", "ya tengo pedido"
    ]

    # Media intención: está evaluando precios o disponibilidad
    medium_intent = [
        "me interesa", "cuánto vale", "qué precio tiene", 
        "pueden enviar", "cuánto demora", "quiero saber si tienen", 
        "podrían cotizarme", "estoy mirando precios"
    ]

    if any(p in text for p in high_intent):
        return "high"
    elif any(p in text for p in medium_intent):
        return "medium"
    return "low"

def detect_logistics_intent(text: str) -> tuple[bool, dict]:
    """
    Detecta si el mensaje del usuario se refiere a temas logísticos
    como tiempos o cobertura de entrega.
    Retorna (True/False, {"type": str, "city": Optional[str]}).
    """
    if not text:
        return False, {}

    import unicodedata, re

    # Limpieza robusta
    text = text.lower().strip()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.replace("¿", "").replace("?", "").replace("¡", "").replace("!", "")

    # Palabras clave extendidas
    logistics_keywords = [
        r"\b(entrega|entregan|entregar|entregado|entregas)\b",
        r"\b(envio|envian|enviar|enviarlo|envios)\b",
        r"\b(despacho|despachos|despachan|despachar)\b",
        r"\b(reparto|repartos|domicilio|domicilios|mensajeria)\b",
        r"\b(cobertura|cubren|alcance)\b",
        r"\b(horario|hora|horas|mañana|tarde|noche|noches|fines?\s+de\s+semana|sabados?|domingos?)\b"
    ]

    # Verificación rápida
    if not any(re.search(pat, text) for pat in logistics_keywords):
        return False, {}

    # Subtipo por prioridad
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

    # Detección de ciudad
    city_match = re.search(
        r"\b(en|a)\s+(bogota|medellin|cali|barranquilla|cartagena|bucaramanga|pereira|manizales|cucuta)\b",
        text,
    )
    city = city_match.group(2).title() if city_match else None

    if city and subtype == "generic":
        subtype = "city_delivery"

    return True, {"type": subtype, "city": city}


def normalize_input(text: str) -> str | None:
    """Busca el nombre canónico de producto con coincidencia flexible."""
    try:
        with open(SYNONYMS_FILE, encoding='utf-8') as f:
            synonyms = json.load(f)
    except Exception:
        synonyms = {}

    msg = text.lower().strip()
    for canonical, variants in synonyms.items():
        for v in variants:
            term = v.lower().strip()

            # 1️⃣ Coincidencia directa
            if term in msg:
                print(f"[normalize_input] Directo: '{term}' → {canonical}")
                return canonical

            # 2️⃣ Coincidencia parcial (palabra incluida o contenida)
            if any(w in msg.split() or w in msg for w in term.split()):
                print(f"[normalize_input] Parcial: '{term}' → {canonical}")
                return canonical

            # 3️⃣ Coincidencia difusa (errores o variantes)
            if SequenceMatcher(None, term, msg).ratio() > 0.7:
                print(f"[normalize_input] Difusa: '{term}' → {canonical}")
                return canonical

    print(f"[normalize_input] Sin coincidencia clara para '{text}'")
    return None

def detect_additional_intents(text: str) -> dict:
    """
    Detecta intenciones adicionales: FAQ ampliado, discount_info y escalamiento.
    Devuelve un dict con flags booleanos.
    """
    text = text.lower()
    intents = {
        "faq": False,
        "discount_info": False,
        "should_escalate": False
    }

    # --- Ampliar FAQ ---
    faq_keywords = [
        "mínimo", "minimos", "compra mínima", "pedido mínimo",  # mínimos de compra
        "forma de pago", "formas de pago", "pago", "pagos",     # métodos de pago
        "contraentrega", "efectivo", "tarjeta", "crédito", "débito",   # pago contraentrega
        "devolución", "devoluciones", "cambio", "cambios", "reembolso", "reembolsos",  # devoluciones/cambios
        "tiempo de entrega", "entregan", "cuánto se demora la entrega"  # tiempos de entrega
    ]

    if any(k in text for k in faq_keywords):
        intents["faq"] = True

    # --- Nueva intención: discount_info ---
    discount_keywords = [
        "promocion", "promoción", "oferta", "descuento", "descuentos",
        "rebaja", "promo", "en oferta"
    ]
    if any(k in text for k in discount_keywords):
        intents["discount_info"] = True

    # --- Escalamiento proactivo ---
    escalate_keywords = [
        "reclamo", "problema", "queja", "certificado adicional",
        "certificado invima", "documento adicional"
    ]
    if any(k in text for k in escalate_keywords):
        intents["should_escalate"] = True

    return intents
