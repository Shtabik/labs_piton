def merge_sorted_list(a, b):
    result = []
    i, j = 0, 0  # индексы для списков a и b

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1

    # добавляем оставшиеся элементы
    while i < len(a):
        result.append(a[i])
        i += 1
    while j < len(b):
        result.append(b[j])
        j += 1

    return result

list1 = [1, 3, 5, 7]
list2 = [2, 4, 6, 8, 10]

merged = merge_sorted_list(list1, list2)
print("Результат:", merged)
