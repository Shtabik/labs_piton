import numpy as np

# Ввод данных
n = int(input("Введите количество участков дороги: "))

lengths = np.array(list(map(float, input("Введите длины участков через пробел: ").split())))
speeds = np.array(list(map(float, input("Введите скорости на участках через пробел: ").split())))

k = int(input("Введите номер участка, на котором автомобиль въехал: "))
p = int(input("Введите номер участка, после которого автомобиль выехал: "))

# Проверка корректности данных
if len(lengths) != n or len(speeds) != n:
    print("Ошибка: количество введённых длин или скоростей не совпадает с n")
    exit()

if not (1 <= k <= n) or not (1 <= p <= n) or k > p:
    print("Ошибка: некорректные номера участков k и p")
    exit()

# Индексация Python (с 0)
start_idx = k - 1
end_idx = p  # срез до end_idx не включает, но p включаем

# Срезы массивов
lengths_segment = lengths[start_idx:end_idx]
speeds_segment = speeds[start_idx:end_idx]

# Длина пути
S = np.sum(lengths_segment)

# Время движения на каждом участке
T_segments = lengths_segment / speeds_segment
T = np.sum(T_segments)

# Средняя скорость
V = S / T

# Вывод результатов
print(f"\nДлина пути: {S:.2f} км")
print(f"Время в пути: {T:.2f} ч")
print(f"Средняя скорость: {V:.2f} км/ч")
