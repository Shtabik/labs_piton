money = int(input("Введите сумму в рублях: "))
nom100 = money // 100 #колво 100
money = money % 100
nom50 = money // 50 #колво 50
money = money % 50
nom10 = money // 10 #колво 10
money = money % 10
nom5 = money // 5 #колво 5
money = money % 5
nom2 = money // 2 #колво 2
money = money % 2
nom1 = money // 1 #колво 1
money = money % 1
print(f"100: {nom100}")
print(f"50: {nom50}")
print(f"10: {nom10}")
print(f"5: {nom5}")
print(f"2: {nom2}")
print(f"1: {nom1}")