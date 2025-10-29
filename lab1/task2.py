text = input("Введите строку: ").lower()
result = (text.replace("a", "")
              .replace("e", "")
              .replace("i", "")
              .replace("o", "")
              .replace("u", ""))
print(result)
#можно привести к нижнему регистру(как сделал я)или же прописать replace("A", "") для гл. высш регистра
