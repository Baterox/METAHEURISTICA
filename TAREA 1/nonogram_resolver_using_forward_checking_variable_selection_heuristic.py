import itertools
import time

class NonogramSolver():
    def __init__(self, N:int, row_constraits:list, col_constraits:list):
        self.N = N
        self.row_constraits = row_constraits
        self.col_constraits = col_constraits
        self.solution = [None]*N**2
        self.domain_lenght = 2
        self.nodes = 0

    def check_constraints(self, current_solution:list, constraits:list) -> bool:
        return [len(list(g)) for k, g in itertools.groupby(current_solution) if k == 1] == constraits

    def viable(self, current_solution:list, index:int, value:int) -> bool:
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

    def forward_checking(self, solution:list, index:list, selected_index:int) -> list:
        if selected_index == self.N**2:
            return solution

        for value in [0,1]:
            current_solution = solution.copy()
            if self.viable(current_solution, index[selected_index], value):
                current_solution[index[selected_index]] = value
                result = self.forward_checking(current_solution, index, selected_index+1)
                self.nodes += 1
                if result:
                    return result
        return None

    def preprocessed(self) -> list:
        dic_row = []
        dic_col = []
        for i in range(self.N):
            dic_row.append({i:self.row_constraits[i]})
            dic_col.append({i:self.col_constraits[i]})

        dic_row_sorted = sorted(dic_row, key=lambda row: sum(list(row.values())[0]) + len(list(row.values())[0]) - 1, reverse=False)
        dic_col_sorted = sorted(dic_col, key=lambda col: sum(list(col.values())[0]) + len(list(col.values())[0]) - 1, reverse=False)

        order_row = [llave for diccionario in dic_row_sorted for llave in diccionario.keys()]
        order_col = [llave for diccionario in dic_col_sorted for llave in diccionario.keys()]

        matrix = []

        for i in (order_row):
            for j in (order_col):
                matrix.append(10 * i + j)

        return (matrix)
        
    def puzzle_solver(self, index_priority: list) -> list:
        new_domains = self.forward_checking(self.solution, index_priority, 0)

        if new_domains:
            grid = {i: new_domains[i] for i in range(len(new_domains))}
            grid = [[grid[row * self.N + col] for col in range(self.N)] for row in range(self.N)]
            return grid
        else:
            return None

if __name__ == "__main__":
    nonogram = NonogramSolver(
        10,
        [[4],[8],[10],[1, 1, 2, 1, 1],[1, 1, 2, 1, 1],[1, 6, 1],[6],[2, 2],[4],[2]],
        [[4],[2],[7],[3, 4],[7, 2],[7, 2],[3, 4],[7],[2],[4]]
    )

    index_priority = nonogram.preprocessed()

    start_time = time.perf_counter()
    solution = nonogram.puzzle_solver(index_priority)
    end_time = time.perf_counter()

    if solution:
        print("\n".join(["".join(["██" if j == 1 else "░░" for j in i]) for i in solution]))
    else:
        print("Has not been found for this puzzle.")

    print(f"Execution Time: {end_time - start_time:.4f} seconds")
    print(f"Generated Nodes: {nonogram.nodes} nodes")