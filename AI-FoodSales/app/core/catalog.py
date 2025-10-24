import csv
def find_product(name):
    try:
        with open("app/data/Catalog.csv", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Producto"].lower() == name.lower():
                    return row
        return None
    except Exception:
        return None
