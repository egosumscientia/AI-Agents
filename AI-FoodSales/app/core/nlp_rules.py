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
