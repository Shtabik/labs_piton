ip = input("Введите IP-адрес: ")
parts = ip.split(".")

if len(parts) != 4:
    print("Некорректный IP")
else:
    if (parts[0].isdigit() and 0 <= int(parts[0]) <= 255 and
        parts[1].isdigit() and 0 <= int(parts[1]) <= 255 and
        parts[2].isdigit() and 0 <= int(parts[2]) <= 255 and
        parts[3].isdigit() and 0 <= int(parts[3]) <= 255):
        print("Корректный IP")
    else:
        print("Некорректный IP")