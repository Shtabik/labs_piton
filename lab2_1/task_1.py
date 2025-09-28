text = input("Введите текст: ")
#split() разбивает строку по любым пробельным символам: пробел(несколько пробелов в ряд == как один пробел), табуляция, перевод строки.
words = text.split()
# Создаём словарь
word_count = {}

for word in words:
    word = word.lower()  # приводим к нижнему регистру, чтобы "Привет" и "привет" считались одним словом
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print("Словарь слов и их количества:", word_count)

print("Количество уникальных слов:", len(word_count))
