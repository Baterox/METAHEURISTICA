import itertools

def get_row_indices(index, N):
    row = index // N
    return [row * N + i for i in range(N)]

def get_col_indices(index, N):
    col = index % N
    return [col + i * N for i in range(N)]

def check_constraint(sequence, clues):
    count = [len(list(g)) for k, g in itertools.groupby(sequence) if k == 1]
    return count == clues

def is_consistent(assignment, index, value, row_clues, col_clues, N):
    row_indices = get_row_indices(index, N)
    col_indices = get_col_indices(index, N)
    
    row = [assignment.get(i, None) for i in row_indices]
    col = [assignment.get(i, None) for i in col_indices]
    
    row[index % N] = value
    col[index // N] = value
    
    if None not in row and not check_constraint(row, row_clues[index // N]):
        return False

    if None not in col and not check_constraint(col, col_clues[index % N]):
        return False

    return True

def select_variable(domains):
    min_remaining_values = float('inf')
    selected_index = -1

    for i, domain in enumerate(domains):
        if 1 < len(domain) < min_remaining_values:
            min_remaining_values = len(domain)
            selected_index = i
    return selected_index if selected_index != -1 else len(domains)

def forward_checking(domains, N, row_clues, col_clues, node_count, backtrack_count):
    selected_index = select_variable(domains)

    if selected_index == len(domains):
        return domains, node_count, backtrack_count

    node_count += 1

    for value in domains[selected_index]:
        assignment = {i: domains[i][0] for i in range(selected_index)}

        if is_consistent(assignment, selected_index, value, row_clues, col_clues, N):
            new_domains = [domain.copy() for domain in domains]
            new_domains[selected_index] = [value]

            for i in range(selected_index + 1, len(domains)):
                new_domains[i] = [v for v in domains[i] if is_consistent(assignment, i, v, row_clues, col_clues, N)]

            if all(new_domains[i] for i in range(selected_index + 1, len(domains))):
                result, new_node_count, new_backtrack_count = forward_checking(new_domains, N, row_clues, col_clues, node_count, backtrack_count)
                if result:
                    return result, new_node_count, new_backtrack_count
        else:
            backtrack_count += 1

    return None, node_count, backtrack_count

def solve_nonogram(row_clues, col_clues):
    N = len(row_clues)
    domains = [[0, 1] for _ in range(N**2)]
    new_domains, node_count, backtrack_count = forward_checking(domains, N, row_clues, col_clues, 0, 0)

    if new_domains:
        assignment = {i: new_domains[i][0] for i in range(len(new_domains))}
        grid = [[assignment[row * N + col] for col in range(N)] for row in range(N)]
        return grid, node_count, backtrack_count
    else:
        print("No solution found")

def main():

    row_clues = [
        [4],
        [8],
        [10],
        [1, 1, 2, 1, 1],
        [1, 1, 2, 1, 1],
        [1, 6, 1],
        [6],
        [2, 2],
        [4],
        [2]
    ]

    col_clues = [
        [4],
        [2],
        [7],
        [3, 4],
        [7, 2],
        [7, 2],
        [3, 4],
        [7],
        [2],
        [4]
    ]

    solution, node_count, backtrack_count = solve_nonogram(row_clues, col_clues)

    if solution:
        for row in solution:
            print("".join("# " if cell == 1 else ". " for cell in row))

    print(f"Nodos generados: {node_count}")
    print(f"Nodos con backtracking: {backtrack_count}")

main()