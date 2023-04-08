import itertools
import time

class NonogramSolver():
    def __init__(self, N:int, row_constraits:list, col_constraits:list):
        self.N = N
        self.row_constraits = row_constraits
        self.col_constraits = col_constraits
        self.solution = [None]*N**2
        self.domain_lenght = 2

    def check_constraints(self, current_solution:list, constraits:list) -> bool:
        return [len(list(g)) for k, g in itertools.groupby(current_solution) if k == 1] == constraits

    def viable(self, current_solution:dict, index:int, value:int) -> bool:
        index_row = (index // self.N)
        row_start =  index_row * self.N
        col_start = index_col = index % self.N

        row = []
        col = []

        for i in range(self.N):
            row.append(current_solution[row_start+i])
            col.append(current_solution[col_start+10*i])
        
        row[index_col] = value
        col[index_row] = value

        if None not in row and not self.check_constraints(row, self.row_constraits[index // self.N]) or \
            None not in col and not self.check_constraints(col, self.col_constraits[index % self.N]):
            return False
        return True

    def forward_checking(self, solution:list, index, selected_index) -> list:
        if selected_index == self.N**2:
            return solution

        for value in [0,1]:
            # grid = [solution[i] for i in range(selected_index)]

            current_solution = solution.copy()
            if self.viable(current_solution, selected_index, value):
                current_solution[selected_index] = value

                # for i in range(self.N**2):
                #     consistents = []
                #     for future_value in [0, 1]:
                #         if self.viable(current_solution, i, future_value):
                #             consistents.append(future_value)
                    
                #     if len(consistents) == 0:
                #         return None
                    
                #     current_solution[i] = consistents

                result = self.forward_checking(current_solution, index, selected_index+1)
                if result:
                    return result
        return None

    def puzzle_solver(self) -> list:
        i = [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
            40, 51, 52, 53, 54, 55, 56, 57, 58, 59,
            60, 41, 42, 43, 44, 45, 46, 47, 48, 49,
            50, 61, 62, 63, 64, 65, 66, 67, 68, 69,
            70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
            80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
            90, 91, 92, 93, 94, 95, 96, 97, 98, 99
        ]
        new_domains = self.forward_checking(self.solution, i, 0)

        #print( new_domains)

        if new_domains:
            grid = {i: new_domains[i] for i in range(len(new_domains))}
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

    start_time = time.perf_counter()
    solution = nonograma.puzzle_solver()
    end_time = time.perf_counter()

    if solution:
        print("\n".join(["".join(["██" if j == 1 else "░░" for j in i]) for i in solution]))
    else:
        print("No se ha encontrado una solución para este puzzle")

    print(f"Tiempo de ejecución: {end_time - start_time:.4f} segundos")