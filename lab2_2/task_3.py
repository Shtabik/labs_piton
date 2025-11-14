import datetime


def log_calls(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # фиксируем время вызова
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # имя функции
            name = func.__name__
            # аргументы
            args_repr = ", ".join(map(str, args))
            kwargs_repr = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            all_args = ", ".join(filter(None, [args_repr, kwargs_repr]))

            # запись в файл
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"[{time}] {name}({all_args})\n")

            # выполняем саму функцию
            return func(*args, **kwargs)

        return wrapper

    return decorator

@log_calls("calls.log")
def add(a, b):
    return a + b

@log_calls("calls.log")
def greet(name, age=None):
    print(f"Привет, {name}! Тебе {age} лет." if age else f"Привет, {name}!")

print(add(2, 3))
greet("Аня", age=20)
