import numpy as np

# Пример расходов по месяцам (12 месяцев)
expenses = np.array([50, 45, 60, 70, 65, 80, 90, 75, 60, 55, 40, 50])

# Названия месяцев
month_names = np.array(["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"])

# ----------------------
# Сравниваем зимние и летние расходы
winter_months = expenses[[11, 0, 1]]  # Декабрь, Январь, Февраль
summer_months = expenses[[5, 6, 7]]   # Июнь, Июль, Август

sum_winter = np.sum(winter_months)
sum_summer = np.sum(summer_months)

if sum_winter > sum_summer:
    print(f"Больше тратится зимой: {sum_winter} руб.")
elif sum_summer > sum_winter:
    print(f"Больше тратится летом: {sum_summer} руб.")
else:
    print(f"Затраты зимой и летом одинаковые: {sum_winter} руб.")

# ----------------------
# Топ-3 месяца с наибольшими расходами
top_indices = np.argsort(expenses)[-3:][::-1]

print("\nТоп-3 месяца с наибольшими расходами:")
for idx in top_indices:
    print(f"{idx + 1} - {month_names[idx]}: {expenses[idx]} руб.")
