import itertools

def print_matrix(matrix):
    print("\n".join([" ".join(["■" if j == 1 else "⛝" if j == -1 else "□" for j in i]) for i in matrix]))
    # chars = {}
    # chars["-1"] = "⛝"
    # chars["0"] = "□"
    # chars["1"] = "■"
    
def copy_matrix(matrix):
    new_matrix = []
    for i in matrix:
        row = []
        for j in i:
            row.append(j)
        new_matrix.append(row)
    return new_matrix

def constrait_remain(matrix):
    for i in matrix:
        for j in i:
            if j == 0:
                return True
    return False

def possible_future_solution(matrix, i,j):
    row_index = 0
    while row_index < len(matrix):
        index = 0
        col_index = 0
        val_constrait = [False]*len(pista_filas[row_index])
        suma = 0
        # print(val_constrait)
        while col_index < len(matrix[row_index]):
            if matrix[row_index][col_index] != -1:
                suma += 1
                # matrix[row_index][col_index] = 1
            else:
                col_index += 1
                suma = 0

            if index < len(pista_filas[row_index]):
                if suma == pista_filas[row_index][index]:
                    matrix[row_index][col_index] = -1
                    val_constrait[index] = True
                    # print(pista_filas[row_index], suma, col_index, val_constrait)
                    col_index += 1
                    suma = 0
                    index += 1
            else:
                matrix[row_index][col_index] = -1

            col_index += 1
        if False in val_constrait:
            return False
        row_index += 1

    col_index = 0
    while col_index < len(matrix):
        index = 0
        row_index = 0
        val_constrait = [False]*len(pista_columnas[col_index])
        suma = 0
        # print(val_constrait)
        while row_index < len(matrix[col_index]):
            if matrix[row_index][col_index] != -1:
                suma += 1
                # matrix[row_index][col_index] = 1
            else:
                row_index += 1
                suma = 0
                continue

            if index < len(pista_columnas[col_index]):
                if suma == pista_columnas[col_index][index]:
                    val_constrait[index] = True
                    # print(pista_columnas[col_index], suma, row_index, val_constrait)
                    row_index += 1
                    suma = 0
                    index += 1
            else:
                matrix[row_index][col_index] = -1
        
            row_index += 1
        if False in val_constrait:
            return False
        col_index += 1
        
    return True

def check_constraint(matrix):
    row_index = 0
    while row_index < len(matrix):
        if [count for count in (len(list(group)) for key, group in itertools.groupby(matrix[row_index]) if key == 1)] != pista_filas[row_index]:
            return False
        row_index += 1

    col_index = 0
    while col_index < len(matrix):
        print([count for count in (len(list(group)) for key, group in itertools.groupby([row[col_index] for row in matrix]) if key == 1)], pista_columnas[col_index])
        if [count for count in (len(list(group)) for key, group in itertools.groupby([row[col_index] for row in matrix]) if key == 1)] != pista_columnas[col_index]:
            return False
        col_index += 1
    return True

def forward_checking(matrix, N, row, col):
    if col == N:
        row += 1
        col = 0
        if row == N:
            return matrix
        
    for value in matrix[row][col]:
        assignment = [[matrix[i][j][0] for i in range(row)] for j in range(col)]
        print(assignment)



    # row_index = 0
    # while row_index < 10:
    #     col_index = 0
    #     while col_index < 10:
    #         for value in [1, -1]:
    #             matrix[row_index][col_index] = value

    #             if possible_future_solution(matrix, row_index, col_index):
                    
    #                 print_matrix(matrix)
    #                 print()
    #                 if check_constraint(matrix):
    #                     return forward_checking(matrix, i, j+1)
    #             else:
    #                 matrix[row_index][col_index] = 0
                
    #         col_index += 1
    #         break
    #     row_index += 1
    #     break

pista_filas = [[4],[8],[10],[1,1,2,1,1],[1,1,2,1,1],[1,6,1],[6],[2,2],[4],[2]]
pista_columnas = [[4],[2],[7],[3,4],[7,2],[7,2],[3,4],[7],[2],[4]]

if __name__ == "__main__":
    N = len( pista_columnas )
    matrix = [[[0, 1]]*N for _ in range(N)]
    print(matrix)

    # matrix = []
    # matrix.append([-1, -1, -1, 1, 1, 1, 1, -1, -1, -1])
    # matrix.append([-1, 1, 1, 1, 1, 1, 1, 1, 1, -1])
    # matrix.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    # matrix.append([1, -1, 1, -1, 1, 1, -1, 1, -1, 1])
    # matrix.append([1, -1, 1, -1, 1, 1, -1, 1, -1, 1])
    # matrix.append([1, -1, 1, 1, 1, 1, 1, 1, -1, 1])
    # matrix.append([-1, -1, 1, 1, 1, 1, 1, 1, -1, -1])
    # matrix.append([-1, -1, 1, 1, -1, -1, 1, 1, -1, -1])
    # matrix.append([-1, -1, -1, 1, 1, 1, 1, -1, -1, -1])
    # matrix.append([-1, -1, -1, -1, 1, 1, -1, -1, -1, -1])

    sol = forward_checking(matrix, N, 0, 0)
    if sol:
        print_matrix(sol)
    else:
        print("No hay solucion")
    print_matrix(matrix)
