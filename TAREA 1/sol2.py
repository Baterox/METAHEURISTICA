def row_constraint(variables, block):
    # Separamos las variables pintadas y contamos los bloques separados por '0's
    filled_cells = "".join(str(v) for v in variables).split("0")
    consecutive_filled = [len(group) for group in filled_cells if group]
    return consecutive_filled == block

def column_constraint(variables, block):
    return row_constraint(variables, block)

def create_problem(row_constraints, column_constraints):
    rows, columns = len(row_constraints), len(column_constraints)
    variables = [[0 for j in range(columns)] for i in range(rows)]
    domain = [0, 1]

    # Restricciones
    for i, row_blocks in enumerate(row_constraints):
        for j in range(columns):
            variables[i][j] = f"X_{i}_{j}"
        for k in range(len(row_blocks)):
            block = row_blocks[k]
            start = 0
            for j in range(columns):
                if j + 1 == columns or variables[i][j+1] != 0:
                    end = j
                    problem_variables = [variables[i][k] for k in range(start, end+1)]
                    problem = [(v, domain) for v in problem_variables]
                    problem.append((None, [v for v in domain if len(problem_variables) + v <= sum(row_blocks[:k+1])]))
                    problem.append((row_constraint, [problem_variables, [block]]))
                    constraints.append(problem)
                    start = j + 1

    for j, column_blocks in enumerate(column_constraints):
        for i in range(rows):
            if variables[i][j] == 0:
                variables[i][j] = f"X_{i}_{j}"
        for k in range(len(column_blocks)):
            block = column_blocks[k]
            start = 0
            for i in range(rows):
                if i + 1 == rows or variables[i+1][j] != 0:
                    end = i
                    problem_variables = [variables[k][j] for k in range(start, end+1)]
                    problem = [(v, domain) for v in problem_variables]
                    problem.append((None, [v for v in domain if len(problem_variables) + v <= sum(column_blocks[:k+1])]))
                    problem.append((column_constraint, [problem_variables, [block]]))
                    constraints.append(problem)
                    start = i + 1

    # Solución
    solution = {}
    while constraints:
        variable, domain = constraints.pop(0)
        for value in domain:
            solution[variable] = value
            if is_consistent(solution, constraints):
                break
        else:
            return None
    return solution

def is_consistent(solution, constraints):
    for constraint in constraints:
        if constraint[2](*[solution[v] for v in constraint[1]]) == False:
            return False
    return True

def display_solution(solution, size):
    if solution is None:
        print("No solution found.")
    else:
        print ("###########")
        rows, columns = size
        for i in range(rows):
            for j in range(columns):
                print(solution[f"X_{i}_{j}"], end=" ")
            print()