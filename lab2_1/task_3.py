numbers_input = input("Введите числа через пробел: ")
numbers = [float(n) if '.' in n else int(n) for n in numbers_input.split()]

#находим юникальные числа
unique_numbers = []
for n in numbers:
    if n not in unique_numbers:
        unique_numbers.append(n)

# Сортируем(sort) по убываниюPython сначала сортирует список по возрастанию (это стандарт).
# Если reverse=True, Python переворачивает отсортированный список в обратном порядке.
unique_numbers.sort(reverse=True)

if len(unique_numbers) >= 2:
    print("Второе по величине число:", unique_numbers[1])
else:
    print("Недостаточно уникальных чисел для второго по величине")
