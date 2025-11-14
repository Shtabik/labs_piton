import time

def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # время начала
        result = func(*args, **kwargs)  # вызов самой функции
        end_time = time.time()  # время окончания
        elapsed_time = (end_time - start_time) * 1000  # разница в миллисекундах
        print(f"Время выполнения функции {func.__name__}: {elapsed_time:.4f} ms")
        return result
    return wrapper

@timing
def slow_function():
    time.sleep(1)  # имитация долгой работы (1 секунда)

@timing
def quick_function():
    time.sleep(0.2)  # имитация более быстрой работы (0.2 секунды)

# вызовы функций
slow_function()
quick_function()
