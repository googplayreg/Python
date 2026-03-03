import re
import json
import os 

current_dir = os.path.dirname(__file__)
path_to_raw_txt = os.path.join(current_dir, 'raw.txt')
path_to_receipt_json = os.path.join(current_dir, 'receipt.json')
# Читаем исходник
with open(path_to_raw_txt, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Извлекаем дату и время
dt_match = re.search(r"(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})", content)
date_time = dt_match.group(1) if dt_match else "Unknown"

# 2. Извлекаем метод оплаты
payment_method = "Банковская карта" if "Банковская карта" in content else "Наличные"

# 3. Извлекаем товары и цены
products = []
items = re.findall(r"\d+\.\n(.*?)\n.*?\n([\d\s]+,00)", content, re.DOTALL)

total_calculated = 0
for name, price_str in items:
    clean_name = name.replace('\n', ' ').strip()
    # Убираем пробелы между тысячами и меняем запятую на точку для float
    price_val = float(price_str.replace(' ', '').replace(',', '.'))
    
    products.append({
        "product": clean_name,
        "price": price_val
    })
    total_calculated += price_val

# Финальный словарь БЕЗ цитат
receipt_data = {
    "store": "EUROPHARMA",
    "date_time": date_time,
    "payment_method": payment_method,
    "items": products,
    "total_sum": total_calculated
}

print(json.dumps(receipt_data, indent=4, ensure_ascii=False))

with open(path_to_receipt_json, 'w', encoding='utf-8') as f:
    json.dump(receipt_data, f, indent=4, ensure_ascii=False)