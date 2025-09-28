def flatten_list(lst):
    # Перебираем элементы списка
    i = 0
    while i < len(lst):
        # Если элемент — список, рекурсивно обрабатываем его
        if isinstance(lst[i], list):
            flatten_list(lst[i])
            lst.pop(i)  # удаляем вложенный список
        else:
            i += 1  # если не список, переходим к следующему элементу


list_a = [1, 2, 3, [4], 5, [6, [7, [], 8, [9]]]]
flatten_list(list_a)
print(list_a)
