# enumerate and zip functions
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for index, name in enumerate(names, start = 1):
    print(f"{index}. {name}")

for name, score in zip(names, scores):
    print(f"{name} scored {score} points")

# type checking and conversions
data = "100"

# 1. Проверка типа
print(type(data))

# 2. Безопасная проверка (рекомендуется)
if isinstance(data, str):
    print("Это строка, конвертируем...")

# 3. Конвертация
num = int(data)      # в целое число
price = float(num)   # в число с плавающей точкой
status = bool(1)     # в логическое (True)

print(f"Итог: {num} - {type(num)}")