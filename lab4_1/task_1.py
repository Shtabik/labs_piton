import numpy as np
import matplotlib.pyplot as plt

# Интервал X в градусах
x_deg = np.linspace(-360, 360, 5000)

# Переводим градусы в радианы для sin/cos
x_rad = np.radians(x_deg)

# Определяем функции
f = np.exp(np.cos(x_rad)) + np.log(np.cos(0.6 * x_rad)**2 + 1) * np.sin(x_rad)
h = -np.log((np.cos(x_rad) + np.sin(x_rad))**2 + 2.5) + 10

# Построение графиков
plt.figure(figsize=(14, 7))

plt.plot(x_deg, f, label='f(x)', linewidth=2)
plt.plot(x_deg, h, label='h(x)', linewidth=2)

# Улучшения графика
plt.title("Графики функций f(x) и h(x) на интервале от -360° до 360°", fontsize=14)
plt.xlabel("x (в градусах)", fontsize=12)
plt.ylabel("Значения функций", fontsize=12)

plt.grid(True, which='both', linestyle='--', linewidth=0.7)
plt.legend(fontsize=12)
plt.tight_layout()

plt.show()
