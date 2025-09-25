s = input("Введите строку(в одном регистре): ")
#1 cпособ
rev = ""
for ch in s:
    rev = ch + rev
print(rev)
if rev==s:
    print("Палиндром")
else:
    print("Не палиндром")

    #2cпособ
"""if s == s[::-1]:
    print("Палиндром")
else:
    print("Не палиндром")
"""