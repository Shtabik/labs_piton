def unique_elements(lst):
    result = []

    def flatten(sublist):
        for item in sublist:
            if isinstance(item, list):   # если список → рекурсия
                flatten(item)
            else:  # если элемент
                if item not in result:   # проверяем на уникальность
                    result.append(item)

    flatten(lst)
    return result

list_a = [1, 2, 3, [4, 3, 1], 5, [6, [7, [10], 8, [9, 2 ,3]]]]
print(unique_elements(list_a))
