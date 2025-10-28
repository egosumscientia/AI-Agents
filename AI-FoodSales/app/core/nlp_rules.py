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
