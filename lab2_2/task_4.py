def transpose(matrix):
    # создаём новую матрицу нужного размера
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = [[0] * rows for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]

    return transposed
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

new_matrix = transpose(matrix)

print("Исходная матрица:")
for row in matrix:
    print(row)

print("\nТранспонированная матрица:")
for row in new_matrix:
    print(row)
