import json
def detect_intent(text):
    if any(k in text for k in ["precio", "cuánto", "cotiza", "total", "cuenta"]):
        return "quote"
    if any(k in text for k in ["tiempo", "entrega", "mínimo", "pago", "invima", "certificado"]):
        return "faq"
    return "other"

def normalize_input(text):
    with open("app/data/synonyms.json", encoding="utf-8") as f:
        synonyms = json.load(f)
    for canonical, terms in synonyms.items():
        if any(term in text for term in terms):
            return canonical
    return text
