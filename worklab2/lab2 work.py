#сгенерируем структуру в которой будут храниться числа и их делители ;через ввод-всех ,если нет добовляем
# ;если есть показываем еще раз
import random
filename="vnutri.txt"
def vvodinfo(fun):
   def wrapper(*args, **kwargs):
       result = fun(*args, **kwargs)
       with open(filename, 'a',encoding="utf-8") as f:
           f.write(str(result)+"\n")
       return result
   return wrapper
@vvodinfo
def delitel(n):
    mas = []
    for i in range(1,n+1):
        if (n % i == 0):
            mas.append(i)
    return mas
id=[9,4,10]






structura={i:delitel(i) for i in id}

print(structura)
while True:
    n = int(input("Введите число: "))


    if n in structura:
        print(f"Делители числа {n}: {structura[n]}")
    else:

        dil = delitel(n)
        structura[n] = dil
        print(f"Добавлено: {n} - {dil}")

    f = input("Еще число? (y/n): ")
    if f == "n":
        break

print("Итоговая структура:", structura)













