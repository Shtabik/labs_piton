import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from faker import Faker
import random

#генерировать бд с инф:вид фрукта(овощей),масса собр урожая по каждому виду,кол-во проданого каждого вида  в кг ,цена за кг;остаток урожая сумму в кг,реализации на кажд виде продукцию, процент реализации( )и сделать график или столбчатые или круговые диаграммы по значениям которые я вычислял
fake = Faker("ru_RU")

tovars = ["Яблоко", "Арбуз", "Дыня", "Огурец", "Помидор"]
data = []

for tovar in tovars:
    pricekg = random.randint(5, 9)
    massa = random.randint(200, 300)
    kolvoprod = random.randint(100, 200)

    if kolvoprod > massa:
        kolvoprod = massa

    realizovano = pricekg * kolvoprod
    ost = pricekg * massa - realizovano
    procent = (realizovano / (pricekg * massa)) * 100

    data.append([tovar, massa, kolvoprod, pricekg, ost, realizovano, procent])

columns = ["вид товара", "масса", "кол-во проданного", "цена за кг",
           "остаток", "реализация", "процент реализации"]

df = pd.DataFrame(data, columns=columns)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(df)


plt.figure(figsize=(8, 5))
barsf=plt.bar(df["вид товара"], df["реализация"], color='skyblue')
plt.bar_label(barsf)

plt.title("Реализация продукции по видам (в у.е.)")
plt.xlabel("Вид товара")
plt.ylabel("Сумма реализации")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()




fig, axes = plt.subplots(1, 5, figsize=(20, 5))
fig.suptitle('Соотношение "Продано" vs "Остаток" по каждому товару', fontsize=16)

for i, (index, row) in enumerate(df.iterrows()):
    sold = row["процент реализации"]
    unsold = 100 - sold
    values = [sold, unsold]
    labels = ["Продано", "Остаток"]
    colors = ['gray', 'pink']

    axes[i].pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    axes[i].set_title(row["вид товара"])

plt.tight_layout()
plt.show()

# ----- График 4: Сравнение Массы и Продаж (Сгруппированные Столбцы) -----
plt.figure(figsize=(10, 6))
x = np.arange(len(df["вид товара"]))
width = 0.4

rects1 = plt.plot(x - width/2, df["масса"], width, label='Всего урожая (кг)', color='red')

rects2 = plt.plot(x + width/2, df["кол-во проданного"], width, label='Реализовано (кг)', color='green')

plt.ylabel('Килограммы', fontsize=12)
plt.title('Соотношение собранного урожая и продаж', fontsize=14)
plt.xticks(x, df["вид товара"], fontsize=10)
plt.legend(frameon=False)
plt.grid(axis='y', linestyle='-', alpha=0.3)


plt.tight_layout()
plt.show()




top3_price = df.sort_values(by="цена за кг", ascending=False).head(3)

plt.figure(figsize=(8, 4))


plt.barh(top3_price["вид товара"], top3_price["цена за кг"], color='orange')

plt.title("Топ-3 самых дорогих товаров (руб/кг)")
plt.xlabel("Цена за кг")
plt.ylabel("Вид товара")
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()


vals = df["цена за кг"].values.reshape(-1, 1)
rows = df["вид товара"].values


vals = df["цена за кг"].values.reshape(-1, 1)
rows = df["вид товара"].values

# ----- Альтернатива: Столбчатая диаграмма с ручной раскраской (имитация тепловой) -----
plt.figure(figsize=(8, 5))

colors = []
for price in df["цена за кг"]:
    # Ручной if/else для выбора цвета в зависимости от цены
    if price == 5:
        colors.append('#ffcccc') # Очень бледный красный
    elif price == 6:
        colors.append('#ff9999') # Светло-красный
    elif price == 7:
        colors.append('#ff6666') # Красный
    elif price == 8:
        colors.append('#ff3333') # Темно-красный
    else: # 9 и выше
        colors.append('#cc0000') # Очень темный

bars = plt.bar(df["вид товара"], df["цена за кг"], color=colors)

plt.title("Градация цен (Ручная раскраска)")
plt.ylabel("Цена за кг")
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Подписываем значения над столбцами
plt.bar_label(bars)

plt.show()

plt.figure(figsize=(5, 6))

# plt.imshow строит тепловую карту
# cmap="YlOrRd" — это палитра (Yellow-Orange-Red).
# Чем больше число, тем краснее. Чем меньше — тем желтее.
heatmap = plt.imshow(vals, cmap="YlOrRd", aspect="auto", vmin=5, vmax=9)

# Настраиваем оси
plt.xticks([]) # Убираем подписи снизу, они нам не нужны (там всего 1 столбец)
plt.yticks(range(len(rows)), rows, fontsize=12) # Подписываем фрукты слева
plt.title("Тепловая карта цен (руб/кг)", fontsize=14)

# Добавляем шкалу цвета справа (чтобы понимать, какой цвет что значит)
plt.colorbar(heatmap, label="Цена за кг")

# Добавляем цифры прямо внутрь квадратиков
for i in range(len(rows)):
    # Выбираем цвет текста: если фон темный (цена > 7), пишем белым, иначе черным
    text_color = "white" if vals[i][0] > 7 else "black"
    plt.text(0, i, f"{vals[i][0]} руб", ha="center", va="center",
             color=text_color, fontweight='bold', fontsize=12)

plt.tight_layout()
plt.show()