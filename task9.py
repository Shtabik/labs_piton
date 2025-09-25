ip = input("Введите IP-адрес: ")
parts = ip.split(".")
if len(parts) != 4:
    print("Некорректный IP")
else:
    valid = True
    for part in parts:
        if not part.isdigit():
            valid = False
            break
        num = int(part)
        if num < 0 or num > 255:
            valid = False
            break
    if valid:
        print("Корректный IP")
    else:
        print("Некорректный IP")