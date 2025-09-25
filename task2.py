text = input("Введите строку: ")
vowels = "aeiouAEIOU"   # гласные
result = ""
for letter in text:          #перебираем все сиволы
    if letter not in vowels:
        result += letter
print(result)