number = int(input("Введите число: "))
if number % 7 == 0:
    print("Магическое число!")
else:
    # Преобразуем число в строку, затем каждый символ в цифру и суммируем
    digits_sum = sum(map(int, str(number)))
    print(digits_sum)