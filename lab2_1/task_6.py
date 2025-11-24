items = input("Введите элементы через пробел: ").split()

unique_items = []
for x in items:
    if x not in unique_items:
        unique_items.append(x)

print("Список без дубликатов:", unique_items)
