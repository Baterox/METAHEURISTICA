def solve_nonogram(nonogram):
    rows, cols = parse_nonogram(nonogram)
    return recursive_solve(rows, cols)

def recursive_solve(rows, cols):
    if not rows:
        return [[]]
    candidates = generate_candidates(rows[0], len(cols))
    solutions = []
    for candidate in candidates:
        if consistent(candidate, cols):
            new_rows = update_rows(rows, candidate)
            new_cols = update_cols(cols, candidate)
            for solution in recursive_solve(new_rows, new_cols):
                solutions.append([candidate] + solution)
    return solutions

def parse_nonogram(nonogram):
    rows, cols = nonogram.split(' '), []
    for i, row in enumerate(rows):
        rows[i] = [int(x) for x in row.split(',')]
    for j in range(len(rows[0])):
        col = []
        for i in range(len(rows)):
            col.append(rows[i][j])
        cols.append(col)
    return rows, cols

def generate_candidates(blocks, length):
    if not blocks:
        return [[]]
    first_block, rest_blocks = blocks[0], blocks[1:]
    candidates = []
    for start in range(length - sum(blocks) - len(blocks) + 1):
        for middle in generate_candidates(rest_blocks, length - start - first_block - 1):
            candidate = [0] * start + [1] * first_block + [0] + middle
            candidates.append(candidate)
    return candidates

def consistent(candidate, cols):
    for j in range(len(cols)):
        col = [row[j] for row in cols]
        if not consistent_helper(candidate, col):
            return False
    return True

def consistent_helper(candidate, col):
    for i in range(len(col)):
        if candidate[i] == 1 and col[i] == 0:
            return False
        if i > 0 and candidate[i] == 1 and candidate[i-1] == 1 and col[i-1] == 0:
            return False
    return True

def update_rows(rows, candidate):
    new_rows = []
    for row, bit in zip(rows, candidate):
        new_row = row.copy()
        if bit == 1:
            new_row.pop(0)
        else:
            new_row[0] -= 1
        new_rows.append(new_row)
def update_cols(cols, candidate):
    new_cols = []
    for j in range(len(cols)):
        new_col = cols[j].copy()
        for i in range(len(new_col)):
            if candidate[i] == 1:
                new_col[i] -= 1
        new_cols.append(new_col)
    return new_cols

def display_solution(solution):
    for row in solution:
        print(''.join(['#' if bit == 1 else '.' for bit in row]))

# Ejemplo de uso
nonogram = "2 1,3,1,1,2 2,1,1,2 2,2,2 2,1,1,2 2,3,2" 
solution = solve_nonogram(nonogram)
if solution:
    display_solution(solution[0])
else:
    print("No se encontró ninguna solución.")