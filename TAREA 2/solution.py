from matplotlib.colors import LinearSegmentedColormap
from classes.UAV import UAV
import matplotlib.pyplot as plt
import numpy as np
import random

class Algorithms:
    def __init__(self, path:str):
        file = open(path, "r")

        self.n_uavs = int(file.readline())
        self.uavs = list()
        
        if("Titan" in path):
            step = 2
        else:
            step = 4

        for i in range(self.n_uavs):
            early_time, preferred_time, late_time = [int(num) for num in file.readline().split()]
            self.uavs.append(UAV(i, early_time, preferred_time, late_time))
            for _ in range(step):
                self.uavs[i].separation_time += [int(num) for num in file.readline().split()]

    def objective_function_value(self, solution:list) -> tuple[int,int]:
        uav_dict = dict()
        cost = 0
        time = 0

        for uav in self.uavs:
            uav_dict[uav.index] = uav

        for i in range(len(solution)):
            current_uav = uav_dict[solution[i]]
            if i == 0:
                time += current_uav.early_time
            else:
                previous_uav = uav_dict[solution[i - 1]]
                time += current_uav.separation_time[previous_uav.index]
                cost += abs(time - current_uav.preferred_time)

        return cost, time
    
    def generate_neighbors(self, current_solution:list, index:int) -> list:
        generated_neighbors = list()

        for i in range(index + 1, len(current_solution)):
            new_array = current_solution.copy()
            new_array[index], new_array[i] = new_array[i], new_array[index]
            generated_neighbors.append(new_array)

        for i in range(index - 1, -1, -1):
            new_array = current_solution.copy()
            new_array[index], new_array[i] = new_array[i], new_array[index]
            generated_neighbors.append(new_array)

        return generated_neighbors

    def deterministic_greedy(self) -> dict:
        uavs = sorted(self.uavs.copy(), key=lambda uav: uav.early_time)
        arrival_order = list()
        time = 0
        score = 0

        for i, uav in enumerate(uavs):
            if i == 0:
                time += uav.early_time
            else:
                time += uav.separation_time[arrival_order[-1].index]
                score += abs(time - uav.preferred_time)

            arrival_order.append(uav)

        return {"arrival_order": [uav.index for uav in arrival_order], "score": score, "time": time}

    def stochastic_greedy(self) -> dict:
        uavs = {len(self.uavs) - i: uav for i, uav in enumerate(sorted(self.uavs.copy(), key=lambda uav: uav.early_time))}
        arrival_order = list()
        time = 0
        score = 0

        for i in range(self.n_uavs):
            weights = list(uavs.keys())
            random_index = random.choices(weights, weights=weights, k=1)[0]
            uav = uavs[random_index]

            if i == 0:
                time += uav.early_time
            else:
                time += uav.separation_time[arrival_order[-1].index]
                score += abs(time - uav.preferred_time)

            arrival_order.append(uav)
            uavs.pop(random_index, None)

        return {"arrival_order": [uav.index for uav in arrival_order], "score": score, "time": time}

    def hill_climbing_some_improvement(self, initial_solution:list, iterations:int) -> tuple[dict,list]:
        best_score, best_time = self.objective_function_value(initial_solution)
        best_solution = initial_solution.copy()
        movements = 0
        graph = list()

        for _ in range(iterations):
            idx = random.randint(0, self.n_uavs - 1)
            neighbors = self.generate_neighbors(best_solution, idx)
            for neighbor in neighbors:
                current_score, time = self.objective_function_value(neighbor)
                if current_score < best_score:
                    best_score = current_score
                    best_solution = neighbor
                    best_time = time
                    movements += 1
                    graph.append( (movements, best_score) )
                    break

        return {"arrival_order": best_solution, "score": best_score, "time": best_time, "movements": movements}, graph

    def hill_climbing_best_improvement(self, initial_solution:list, iterations:int) -> tuple[dict, list]:
        best_score, best_time = self.objective_function_value(initial_solution)
        best_solution = initial_solution.copy()
        movements = 0
        graph = list()

        for _ in range(iterations):
            idx = random.randint(0, self.n_uavs - 1)
            neighbors = self.generate_neighbors(best_solution, idx)

            for neighbor in neighbors:
                current_score, time = self.objective_function_value(neighbor)
                if current_score < best_score:
                    best_solution = neighbor
                    best_score = current_score
                    best_time = time
                    movements += 1
                    graph.append( (movements, best_score) )

        return {"arrival_order": best_solution, "score": best_score, "time": best_time, "movements": movements}, graph

    def tabu_search(self, initial_solution:list, iterations:int, tabu_list_max_len:int) -> tuple[dict, list]:
        best_score, best_time = self.objective_function_value(initial_solution)
        best_solution = initial_solution.copy()
        movements = 0
        tabu_list = list()
        graph = list()

        for _ in range(100):
            idx = random.randint(0, self.n_uavs - 1)
            neighbors = self.generate_neighbors(list(best_solution), idx)

            neighbors_dict = dict()
            for neighbor in neighbors:
                current_score, time = self.objective_function_value(neighbor)
                neighbors_dict[tuple(neighbor)] = current_score

            sorted_dict = dict(sorted(neighbors_dict.items(), key=lambda x: x[1]))

            for k in sorted_dict:
                if k not in tabu_list:
                    current_solution = k
                    if len(tabu_list) == tabu_list_max_len:
                        tabu_list.pop(0)
                    tabu_list.append(k)
                    break

            current_solution_score, current_solution_time = self.objective_function_value(current_solution)

            if current_solution_score < best_score:
                best_solution = current_solution
                best_score = current_solution_score
                best_time = current_solution_time
                movements += 1
                graph.append( (movements, best_score) )

        return {"arrival_order": best_solution, "score": best_score, "time": best_time, "movements": movements}, graph

def plot_movements(graph:list, algorith_name:str):
    x = [item[0] for item in graph]
    y = [item[1] for item in graph]

    color_map = LinearSegmentedColormap.from_list('ColorMap', ['red', 'yellow', 'green'])
    fig, ax = plt.subplots()

    for i in range(len(x) - 1):
        color = color_map(i / (len(x) - 1))  # Interpolación del color
        ax.plot([x[i], x[i+1]], [y[i], y[i+1]], color=color, linewidth=2)

    ax.set_title(f'Mejora por movimiento - {algorith_name}')
    ax.set_xlabel('Movimiento')
    ax.set_ylabel('Valor FO')

    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    points_to_annotate = np.linspace(0, len(graph) - 1, 4, dtype=int)


    for i in points_to_annotate:
        tup = graph[i]
        ax.annotate(tup[1], (tup[0], tup[1]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.show()

def excute_all_algorithms(path:str, iterations:int, tabu_list_len:int):
    problem = Algorithms(path)

    deterministic_greedy = problem.deterministic_greedy()
    print("[1] GREEDY DETERMINISTA")
    print(f"Solución: {deterministic_greedy['arrival_order']}\nMejor Puntaje: {deterministic_greedy['score']}\nTiempo: {deterministic_greedy['time']}\n")

    stochastic_greedys = sorted([problem.stochastic_greedy() for _ in range(5)], key=lambda sg: sg["score"])
    for index,solution in enumerate(stochastic_greedys):
        print(f"[{index+1}] GREEDY ESTOCASTICO")
        print(f"Solución: {solution['arrival_order']}\nMejor Puntaje: {solution['score']}\nTiempo: {solution['time']}\n")

    print("[O] SOLUCIÓN INICIAL - GREEDY DETERMINISTA")
    initial_solution = deterministic_greedy["arrival_order"]

    hill_climbing_some_improvement, hill_climbing_some_improvement_plot = problem.hill_climbing_some_improvement(initial_solution, iterations)
    plot_movements(hill_climbing_some_improvement_plot, "Hill Climbing Alguna-Mejora - Greedy Determinista")
    print("[1] HILL CLIMBING ALGUNA-MEJORA - GREEDY DETERMINISTA")
    print(f"Solución: {hill_climbing_some_improvement['arrival_order']}\nMejor Puntaje: {hill_climbing_some_improvement['score']}\nTiempo: {hill_climbing_some_improvement['time']}\nMovimientos: {hill_climbing_some_improvement['movements']}\n")

    hill_climbing_best_improvement, hill_climbing_best_improvement_plot = problem.hill_climbing_best_improvement(initial_solution, iterations)
    plot_movements(hill_climbing_best_improvement_plot, "Hill Climbing Mejor-Mejora - Greedy Determinista")
    print("[1] HILL CLIMBING MEJOR-MEJORA - GREEDY DETERMINISTA")
    print(f"Solución: {hill_climbing_best_improvement['arrival_order']}\nMejor Puntaje: {hill_climbing_best_improvement['score']}\nTiempo: {hill_climbing_best_improvement['time']}\nMovimientos: {hill_climbing_best_improvement['movements']}\n")

    tabu_search, tabu_search_plot = problem.tabu_search(initial_solution, iterations, tabu_list_len)
    plot_movements(tabu_search_plot, "Búsqueda Tabú - Greedy Determinista")
    print("[1] BÚSQUEDA TABÚ - GREEDY DETERMINISTA")
    print(f"Solución: {tabu_search['arrival_order']}\nMejor Puntaje: {tabu_search['score']}\nTiempo: {tabu_search['time']}\nMovimientos: {tabu_search['movements']}\n")



    print("[O] SOLUCIÓN INICIAL - GREEDY ESTOCASTICO")
    initial_solution = stochastic_greedys[0]["arrival_order"]

    hill_climbing_some_improvement, hill_climbing_some_improvement_plot = problem.hill_climbing_some_improvement(initial_solution, iterations)
    plot_movements(hill_climbing_some_improvement_plot, "Hill Climbing Alguna-Mejora - Greedy Estocastico")
    print("[1] HILL CLIMBING ALGUNA-MEJORA - GREEDY ESTOCASTICO")
    print(f"Solución: {hill_climbing_some_improvement['arrival_order']}\nMejor Puntaje: {hill_climbing_some_improvement['score']}\nTiempo: {hill_climbing_some_improvement['time']}\nMovimientos: {hill_climbing_some_improvement['movements']}\n")

    hill_climbing_best_improvement, hill_climbing_best_improvement_plot = problem.hill_climbing_best_improvement(initial_solution, iterations)
    plot_movements(hill_climbing_best_improvement_plot, "Hill Climbing Mejor-Mejora - Greedy Estocastico")
    print("[1] HILL CLIMBING MEJOR-MEJORA - GREEDY ESTOCASTICO")
    print(f"Solución: {hill_climbing_best_improvement['arrival_order']}\nMejor Puntaje: {hill_climbing_best_improvement['score']}\nTiempo: {hill_climbing_best_improvement['time']}\nMovimientos: {hill_climbing_best_improvement['movements']}\n")

    tabu_search, tabu_search_plot = problem.tabu_search(initial_solution, iterations, tabu_list_len)
    plot_movements(tabu_search_plot, "Búsqueda Tabú - Greedy Estocastico")
    print("[1] BÚSQUEDA TABÚ - GREEDY ESTOCASTICO")
    print(f"Solución: {tabu_search['arrival_order']}\nMejor Puntaje: {tabu_search['score']}\nTiempo: {tabu_search['time']}\nMovimientos: {tabu_search['movements']}\n")

if __name__ == "__main__":
    print("[*] FILE NAME: TITAN\n")
    excute_all_algorithms("./data/t2_Titan.txt", 100, 70)

    # print("[*] FILE NAME: EUROPA\n")
    # excute_all_algorithms("./data/t2_Europa.txt", 100, 10)

    # print("[*] FILE NAME: DEIMOS\n")
    # excute_all_algorithms("./data/t2_Deimos.txt", 100, 70)