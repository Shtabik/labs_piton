import numpy as np
from scipy.integrate import quad, dblquad

# --- 1. Определенный (одиночный) интеграл ---
# Интеграл: f(x) = x^2 от 0 до 1

def f(x):
    return x**2

# Вычисляем интеграл
# quad возвращает (результат, погрешность)
result_quad, error_quad = quad(f, 0, 1)

print("--- Одиночный интеграл ---")
print(f"Решение интеграла (x^2) от 0 до 1: {result_quad}")
print(f"(Аналитическое решение: 1/3 = {1/3})")
print(f"Погрешность вычисления: {error_quad}\n")


# --- 2. Двойной интеграл ---
# Интеграл: f(x, y) = x + y
# Пределы: y от 0 до 2 (внешний), x от 0 до 1 (внутренний)

# ВАЖНО: dblquad ожидает функцию в порядке f(y, x)
def g(y, x):
    return x + y

# Вычисляем интеграл
# dblquad(func, a, b, gfun, hfun)
# a, b - пределы ВНЕШНЕГО интеграла (для y)
# gfun, hfun - пределы ВНУТРЕННЕГО интеграла (для x)
# Если пределы x - константы (как у нас), можно писать просто числа:


result_dbl, error_dbl = dblquad(g, 0, 2, lambda y: 0, lambda y: 1)

print("--- Двойной интеграл ---")
print(f"Решение интеграла (x+y) dx dy (x от 0 до 1, y от 0 до 2): {result_dbl}")
print(f"(Аналитическое решение: 3)")
print(f"Погрешность вычисления: {error_dbl}\n")