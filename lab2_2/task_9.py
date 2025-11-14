def type_check(*expected_types):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Проверяем аргументы на соответствие ожидаемым типам
            for arg, expected_type in zip(args, expected_types):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Ожидался тип {expected_type}, но получен {type(arg)}")

            # Проверяем ключевые слова (если они есть)
            for key, value in kwargs.items():
                expected_type = expected_types[len(args) + list(kwargs).index(key)]
                if not isinstance(value, expected_type):
                    raise TypeError(f"Ожидался тип {expected_type} для {key}, но получен {type(value)}")

            return func(*args, **kwargs)

        return wrapper

    return decorator

@type_check(int, int)
def add(a, b):
    return a + b

# Правильные параметры
print(add(2, 3))  # 5

# Неправильные параметры
try:
    print(add(2, "3"))
except TypeError as e:
    print(f"Ошибка: {e}")
