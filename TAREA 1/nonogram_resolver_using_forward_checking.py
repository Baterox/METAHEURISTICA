import itertools

class NonogramSolver():
    def __init__(self, N:int, row_constraits:list, col_constraits:list):
        self.N = N
        self.row_constraits = row_constraits
        self.col_constraits = col_constraits
        self.solution = [[0, 1]]*N**2
        self.domain_lenght = 2

    def check_constraints(self, current_solution:list, constraits:list) -> bool:
        return [len(list(g)) for k, g in itertools.groupby(current_solution) if k == 1] == constraits

    def get_current_index(self, current_solution:list) -> int:
        current_solution_len = [len(domain) for domain in current_solution]
        try:
            return current_solution_len.index(self.domain_lenght)
        except:
            return self.N**2

    def check_non_empty_domains(self, selected_index:int, new_solution:list) -> bool:
        for i in range(selected_index + 1, len(new_solution)):
            if not new_solution[i]:
                return False
        return True
    
    def viable(self, grid:list, index:int, value:int) -> bool:
        index_row = (index // self.N)
        row_start =  index_row * self.N
        col_start = index_col = index % self.N

        row = []
        col = []

        for i in range(self.N):
            if row_start+i < len(grid):
                row.append(grid[row_start+i])
            else:
                row.append(None)
        
            if col_start+10*i < len(grid):
                col.append(grid[col_start+10*i])
            else:
                col.append(None) 

        row[index_col] = value
        col[index_row] = value

        if None not in row and not self.check_constraints(row, self.row_constraits[index // self.N]) or \
            None not in col and not self.check_constraints(col, self.col_constraits[index % self.N]):
            return False
        return True

    def forward_checking(self, solution:list) -> list:
        selected_index = self.get_current_index(solution)
        if selected_index == len(solution):
            return solution

        for value in solution[selected_index]:
            grid = [solution[i][0] for i in range(selected_index)]


            if self.viable(grid, selected_index, value):
                new_solution = [domain.copy() for domain in solution]
                new_solution[selected_index] = [value]

                # for i in range(selected_index + 1, len(solution)):
                #     consistents = []
                #     for v in solution[i]:
                #         if self.viable(grid,i,v):
                #             consistents.append(v)
                #     new_solution[i] = consistents

                if self.check_non_empty_domains(selected_index, new_solution):
                    result = self.forward_checking(new_solution)
                    if result:
                        return result
        return None

    def puzzle_solver(self) -> list:
        new_domains = self.forward_checking(self.solution)
        #print( new_domains)

        if new_domains:
            grid = {i: new_domains[i][0] for i in range(len(new_domains))}
            grid = [[grid[row * self.N + col] for col in range(self.N)] for row in range(self.N)]
            return grid
        else:
            return None

if __name__ == "__main__":
    nonograma = NonogramSolver(
        10,
        [[4],[8],[10],[1, 1, 2, 1, 1],[1, 1, 2, 1, 1],[1, 6, 1],[6],[2, 2],[4],[2]],
        [[4],[2],[7],[3, 4],[7, 2],[7, 2],[3, 4],[7],[2],[4]]
    )

    solution = nonograma.puzzle_solver()

    if solution:
        print("\n".join(["".join(["██" if j == 1 else "░░" for j in i]) for i in solution]))
    else:
        print("No se ha encontrado una solución para este puzzle")



