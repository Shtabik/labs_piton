import random  # для генерации случайного числа
number = random.randint(1, 100)
while True:
    guess = int(input("Введите вашу догадку: "))
    if guess < number:
        print("Больше")
    elif guess > number:
        print("Меньше")
    else:
        print("Поздравляю! Вы угадали число:", number)
        break