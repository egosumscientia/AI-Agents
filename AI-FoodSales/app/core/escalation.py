def should_escalate(text):
    triggers = ['contrato','certificado adicional','reclamo','problema','descuento especial']
    return any(t in text for t in triggers)
