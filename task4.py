money = int(input("Введите сумму в рублях: "))
nominals = [100, 50, 10, 5, 2, 1]
for d in nominals:
    count = money // d      # сколько нужно
    money %= d             #ост. кэш
    print(f"{d}: {count}")