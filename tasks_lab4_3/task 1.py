import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from faker import Faker
import random

fake = Faker("ru_RU")

# ----- Генерация данных -----
years = [2020, 2021, 2022, 2023, 2024]
forms = ["Бюджет", "Платно"]
specialities = ["Информатика", "Экономика", "Менеджмент", "Физика", "Математика"]
subjects = ["Математика", "Физика", "Русский язык"]

data = []

for year in years:
    for _ in range(200):  # 200 студентов на год
        fio = fake.name()
        form = random.choice(forms)
        scores_ce = {sub: random.randint(20, 100) for sub in subjects}
        attest = round(random.uniform(5.0, 10.0), 2)
        total_score = round(sum(scores_ce.values()) * 0.7 + attest * 10 * 0.3, 2)
        speciality = random.choice(specialities)
        address = fake.address().replace("\n", ", ")
        phone = fake.phone_number()

        data.append([
            fio, year, form,
            scores_ce["Математика"],
            scores_ce["Физика"],
            scores_ce["Русский язык"],
            attest, total_score,
            speciality, address, phone
        ])

columns = [
    "ФИО", "Год", "Форма обучения",
    "ЦЭ Математика", "ЦЭ Физика", "ЦЭ Русский",
    "Аттестат", "Общий балл",
    "Специальность", "Адрес", "Телефон"
]

df = pd.DataFrame(data, columns=columns)

# Выводим ПОЛНОСТЬЮ весь DataFrame
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(df.iloc[0:5,:])

# ---------------- Графики ----------------

# 1. Средний балл ЦЭ по предметам
avg_scores = df.groupby("Год")[["ЦЭ Математика", "ЦЭ Физика", "ЦЭ Русский"]].mean()

plt.figure()
plt.title("Средний балл ЦЭ по предметам")
plt.plot(avg_scores.index.astype(int), avg_scores["ЦЭ Математика"], marker="o", label="Математика")
plt.plot(avg_scores.index.astype(int), avg_scores["ЦЭ Физика"], marker="o", label="Физика")
plt.plot(avg_scores.index.astype(int), avg_scores["ЦЭ Русский"], marker="o", label="Русский язык")
plt.xlabel("Год")
plt.ylabel("Средний балл")
plt.grid()
plt.legend()
plt.show()


# 2. Динамика среднего балла аттестата
avg_attest = df.groupby("Год")["Аттестат"].mean()

plt.figure()
plt.title("Динамика среднего балла аттестата")
plt.plot(avg_attest.index.astype(int), avg_attest, marker="o")
plt.xlabel("Год")
plt.ylabel("Аттестат")
plt.grid()
plt.show()


# 3. Динамика проходного балла (берем минимальный общий балл)
passing_score = df.groupby("Год")["Общий балл"].min()

plt.figure()
plt.title("Динамика проходного балла")
plt.plot(passing_score.index.astype(int), passing_score, marker="o", color="red")
plt.xlabel("Год")
plt.ylabel("Проходной балл")
plt.grid()
plt.show()


# 4. Кол-во поступивших по специальностям
spec_count = df["Специальность"].value_counts()

plt.figure()
plt.title("Количество поступивших по специальностям")
spec_count.plot(kind="bar")
plt.ylabel("Количество студентов")
plt.grid(axis="y")
plt.show()


# 5. Статистика по формам обучения
forms_count = df["Форма обучения"].value_counts()

plt.figure()
plt.title("Формы обучения")
forms_count.plot(kind="pie", autopct="%1.1f%%")
plt.ylabel("")
plt.show()
