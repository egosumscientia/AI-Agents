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

    import unicodedata
    import re

    # 🔧 Limpieza robusta
    text = text.lower().strip()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.replace("¿", "").replace("?", "").replace("¡", "").replace("!", "")

    logistics_keywords = [
        r"\b(entrega|entregan|entregar|entregado|entregas)\b",
        r"\b(envio|envian|enviar|envios)\b",
        r"\b(despacho|despachos|despachan|despachar)\b",
        r"\b(reparto|domicilio|domicilios|mensajeria)\b",
        r"\b(fines?\s+de\s+semana|sabados?|domingos?)\b",
    ]

    # 🧩 Debug útil
    print(f"[DEBUG] Texto limpio recibido: {text}")
    for pat in logistics_keywords:
        if re.search(pat, text):
            print(f"[DEBUG] Coincidencia con patrón: {pat}")

    # 🔍 Verifica si hay alguna palabra logística
    if not any(re.search(pat, text) for pat in logistics_keywords):
        return False, {}

    # 🧩 Subtipo de intención
    if re.search(r"\b(fines?\s+de\s+semana|sabados?|domingos?)\b", text):
        subtype = "weekend"
    elif re.search(r"\b(cuanto\s+tardan?|tiempos?\s+de\s+entrega|plazo)\b", text):
        subtype = "delivery_time"
    elif re.search(r"\b(otras?\s+ciudades|fuera|nacional|envian\s+a)\b", text):
        subtype = "coverage"
    else:
        subtype = "generic"

    # 🏙️ Ciudad (si la menciona)
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
