numbers_input = input("Введите числа через пробел: ")

numbers = []
for n in numbers_input.split():
    if '.' in n:
        numbers.append(float(n))
    else:
        numbers.append(int(n))

unique_numbers = set(numbers)
print("Уникальные числа:", unique_numbers)

repeated_numbers = set(x for x in numbers if numbers.count(x) > 1) #count это готовый метод
print("Повторяющиеся числа:", repeated_numbers)
#Чётные/нечётные — только для целых чисел,isinstance() — это встроенная функция Python, которая проверяет, является ли объект экземпляром определённого типа (класса или подкласса).
even_numbers = [x for x in numbers if isinstance(x, int) and x % 2 == 0]
odd_numbers = [x for x in numbers if isinstance(x, int) and x % 2 != 0]
print("Чётные числа:(выписываем все -даже если число встречается пару раз в исходном списке чисел)", even_numbers)
print("Нечётные числа:(выписываем все -даже если число встречается пару раз в исходном списке чисел)", odd_numbers)

negative_numbers = [x for x in numbers if x < 0]
print("Отрицательные числа:(выписываем все -даже если число встречается пару раз в исходном списке чисел)", negative_numbers)

float_numbers = [x for x in numbers if isinstance(x, float)]
print("Числа с плавающей точкой:(выписываем все -даже если число встречается пару раз в исходном списке чисел)", float_numbers)

sum_div_5 = sum(x for x in numbers if isinstance(x, int) and x % 5 == 0)
print("Сумма чисел, кратных 5:", sum_div_5)

print("Самое большое число:", max(numbers))

print("Самое маленькое число:", min(numbers))
