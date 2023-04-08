from functools import partial

class ConstraintProblem:
    def __init__(self):
        self.variables = {}
        self.constraints = []

    def add_variables(self, variables, domain):
        for var in variables:
            self.variables[var] = domain

    def add_constraint(self, constraint, variables):
        self.constraints.append((constraint, variables))

    def is_consistent(self, assignment, var, value):
        for constraint, constraint_vars in self.constraints:
            if var in constraint_vars:
                assigned_vars = [v for v in constraint_vars if v in assignment]
                if assigned_vars:
                    assigned_values = [assignment[v] for v in assigned_vars]
                    if not constraint(*(assigned_values + [value])):
                        return False
        return True

    def forward_checking(self, assignment, remaining_domains):
        if len(assignment) == len(self.variables):
            return assignment

        var = min(remaining_domains, key=lambda v: len(remaining_domains[v]))

        for value in remaining_domains[var]:
            if self.is_consistent(assignment, var, value):
                new_assignment = assignment.copy()
                new_assignment[var] = value

                new_remaining_domains = remaining_domains.copy()
                new_remaining_domains.pop(var)

                for v in new_remaining_domains:
                    new_remaining_domains[v] = [x for x in remaining_domains[v] if self.is_consistent(new_assignment, v, x)]

                result = self.forward_checking(new_assignment, new_remaining_domains)
                if result:
                    return result

        return None

    def get_solution(self):
        initial_domains = {var: self.variables[var] for var in self.variables}
        return self.forward_checking({}, initial_domains)
    
def row_constraint(*variables, block):
    # Separamos las variables pintadas y conmtamos los bloques separados por '0's
    filled_cells = "".join(str(v) for v in variables).split("0")
    consecutive_filled = [len(group) for group in filled_cells if group]
    return consecutive_filled == block

def column_constraint(*variables, block):
    return row_constraint(*variables, block=block)

def create_problem(row_c, column_c):
    rows, columns = len(row_c), len(column_c)
    problem = ConstraintProblem()

    # Variables
    variables = [f"X_{row}_{col}" for row in range(rows) for col in range(columns)]

    # Dominios
    domain = [0, 1]

    problem.add_variables(variables, domain)

    # Restricciones
    for i, row_blocks in enumerate(row_constraints):
        problem.add_constraint(partial(row_constraint, block=row_blocks), [f"X_{i}_{j}" for j in range(columns)])

    for j, col_blocks in enumerate(column_constraints):
        problem.add_constraint(partial(row_constraint, block=col_blocks), [f"X_{i}_{j}" for i in range(rows)])

    return problem.get_solution()

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

row_constraints = [
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

column_constraints = [
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



sol = create_problem(row_constraints, column_constraints)
display_solution(sol, (len(row_constraints), len(column_constraints)))