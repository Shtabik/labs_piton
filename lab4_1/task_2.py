import numpy as np
import matplotlib.pyplot as plt

# Интервал значений x
x = np.linspace(-10, 10, 20000)

# Значения функции
y = 5 / (x**2 - 9)

# Убираем точки около асимптот (x = 3 и x = -3), чтобы не было скачков
epsilon = 0.02  # ширина "запрещённой зоны"
y[np.abs(x - 3) < epsilon] = np.nan
y[np.abs(x + 3) < epsilon] = np.nan

# Построение графика
plt.figure(figsize=(12, 6))
plt.plot(x, y, linewidth=2)

# Асимптоты
plt.axvline(3, color='gray', linestyle='--', linewidth=1)
plt.axvline(-3, color='gray', linestyle='--', linewidth=1)

# Настройки графика
plt.ylim(-10, 10)   # ограничим по Y, чтобы график был читаемым
plt.grid(True)
plt.title("Улучшенный график функции f(x) = 5 / (x² - 9)")
plt.xlabel("x")
plt.ylabel("f(x)")

plt.show()
