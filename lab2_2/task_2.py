def merge_dicts(d1, d2):
    for key, value in d2.items():  # проходим по ключам второго словаря
        if key in d1:  # если ключ уже есть в первом словаре
            # если и там, и там словари → рекурсия
            if isinstance(d1[key], dict) and isinstance(value, dict):
                merge_dicts(d1[key], value)
            else:
                # иначе просто заменяем значением из второго словаря
                d1[key] = value
        else:
            # если ключа нет в первом словаре → добавляем
            d1[key] = value
    return d1
dict_a = {"a": 1, "b": {"c": 1, "f": 4}}
dict_b = {"d": 1, "b": {"c": 2, "e": 3}}

merge_dicts(dict_a, dict_b)
print(dict_a)