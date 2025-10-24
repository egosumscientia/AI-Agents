import csv, os
def find_product(name):
    try:
        path = os.path.join('app','data','Catalog.csv')
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Producto','').strip().lower() == name.lower():
                    return row
        return None
    except Exception:
        return None
