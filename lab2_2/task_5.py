def cache(func):
    storage = {}  # словарь для кэша

    def wrapper(*args, **kwargs):
        # создаём ключ из аргументов (tuple, потому что он хэшируемый)
        key = (args, tuple(sorted(kwargs.items())))

        if key in storage:
            print(f"Результат из кэша для {func.__name__}{args, kwargs}")
            return storage[key]

        # если нет в кэше → вычисляем и сохраняем
        result = func(*args, **kwargs)
        storage[key] = result
        return result

    return wrapper

@cache
def slow_square(x):
    print(f"Вычисляю {x} * {x}...")
    return x * x

print(slow_square(4))   # первый вызов → вычисляет
print(slow_square(4))   # второй вызов → берёт из кэша
print(slow_square(5))   # вычисляет
print(slow_square(5))   # берёт из кэша
