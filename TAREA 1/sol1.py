# FUNCIÓN QUE IMPRIME LA MATRIZ CON FORMATO
def print_matrix(matrix):
    for row in matrix:
        print(row)

# FUNCIÓN QUE RETORNA LA SUMATORIA DE TODOS LOS VALORES CONTENIDOS EN UN ARREGLO
def sum_array_values(array):
    sum = 0
    for value in array:
        sum += value
    return value

# FUNCIÓN QUE RETORNA EN UN ARREGLO, EL TAMAÑO DE LAS CADENAS RELLENADAS
def split_row(arr):
    counts_arr = [count for count in (len(list(group)) for key, group in itertools.groupby(arr) if key == 1)]
    return counts_arr

# FUNCIÓN QUE EXTRAE UNA COLUMNA J DE UNA MATRIZ
def get_column(matrix, j):
    return [row[j] for row in matrix]

def define_dominio(matrix, i, j):
    for row in range(sum_array_values(pista_filas[i]), N):
        matrix[row][j] = -1
    for col in range(sum_array_values(pista_columnas[j]), N):
        matrix[i][col] = -1



if __name__ == "__main__":
    pista_filas = [[4],[8],[10],[1,1,2,1,1],[1,1,2,1,1],[1,6,1],[6],[2,2],[4],[2]]
    pista_columnas = [[4],[2],[7],[3,4],[7,2],[7,2],[3,4],[7],[2],[4]]

    N = len( pista_columnas )
    matrix = [[0]*N for _ in range(N)]