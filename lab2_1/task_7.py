text = input("Введите строку: ")

result = ""
count = 1

for i in range(1, len(text)): #вместо счетчика как других языках I++
    if text[i] == text[i - 1]:
        count += 1
    else:                        # символ изменился → записываем результат
        result += text[i - 1] + str(count)
        count = 1


if text:
    result += text[-1] + str(count) #это последний символ строки

print(result)
