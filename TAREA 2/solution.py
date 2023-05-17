from matplotlib.colors import LinearSegmentedColormap
from classes.UAV import UAV
import matplotlib.pyplot as plt
import numpy as np
import random

class Algorithms:
    # EL ALGORITMO SE INICIALIZA CON EL ARCHIVO TXT QUE SE LE ENTREGUE.
    # EL ARCHIVO CONTIENE LA CANTIDAD DE UAVS EN EL PROBLEMA.
    # PARA CADA UAV CONTIENE UN TIEMPO TEMPRANO, PREFERENTE, ÚLTIMO Y UNA COLECCIÓN DE TIEMPOS DE SEPARACIÓN.
    def __init__(self, path:str):
        # SE LEE EL ARCHIVO UN SU RUTA ESPECIFICA
        file = open(path, "r")
        # SE LEE LA PRIMERA LINEA DEL ARCHIVO QUE CONTIENE LA CANTIDAD DE UAVS
        self.n_uavs = int(file.readline())
        # SE INICIALIZA UNA LISTA VACÍA DE UAVS
        self.uavs = list()
        
        # EL ARCHIVO TITAN ES DISTINTO AL RESTO, ESTE TIENE 2 LINEAS QUE CONTIENEN LOS TIEMPOS DE SEPARACIÓN
        # RESPECTO AL RESTO DE UAVS, EN CAMBIO LOS DEMÁS 4
        if("Titan" in path):
            step = 2
        else:
            step = 4

        # SE ITERA N UAVS PARA EXTRAER SU INFORMACIÓN, CODIFICARLA EN UNA CLASE UAV Y AÑADIRLA A LA LISTA VACÍA DE UAVS
        for i in range(self.n_uavs):
            early_time, preferred_time, late_time = [int(num) for num in file.readline().split()]
            self.uavs.append(UAV(i, early_time, preferred_time, late_time))
            for _ in range(step):
                self.uavs[i].separation_time += [int(num) for num in file.readline().split()]

    # FUNCIÓN QUE RECIBE UNA SOLUCIÓN Y RETORNA EL COSTO/PENALIZACIÓN QUE TIENE EL ORDEN DE LLEGADA DE LOS UAVS.
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
    
    # FUNCIÓN QUE GENERA UN VECINDARIO DE SOLUCIONES EN BASE A UNA SOLUCIÓN ACTUAL Y UN INDICE.
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

    # ALGORITMO GREEDY DETERMINISTA.
    def deterministic_greedy(self) -> dict:
        # ORDENA TODOS LOS UAVS, EN BASE SUS TIEMPOS TEMPRANOS DE LLEGADA.
        uavs = sorted(self.uavs.copy(), key=lambda uav: uav.early_time)
        # SE INICIALIZA UNA LISTA VACÍA QUE REPRESENTARÁ LA SOLUCIÓN.
        arrival_order = list()
        # SE INICIALIZA EL TIEMPO Y PUNTAJE EN 0.
        time = 0
        score = 0

        # SE RECORRE CADA UAV.
        for i, uav in enumerate(uavs):
            # EL TIEMPO TOTAL, INICIARÁ COMO EL TIEMPO TEMPRANO DE LLEGADA DEL PRIMER UAV EN ATERRIZAR.
            if i == 0:
                time += uav.early_time
            # PARA EL RESTO DE ITERACIONES, EL TIEMPO AUMENTARÁ COMO LOS TIEMPOS DE SEPARACIÓN DEL UAV ACTUAL CON EL ANTERIOR UAV EN ATERRIZAR.
            # EL PUNTAJE SERÁ LA RESTA ABSOLUTA ENTRE EL TIEMPO TOTAL Y EL TIEMPO PREFERENTE DE LLEGADA DEL UAV ACTUAL.
            else:
                time += uav.separation_time[arrival_order[-1].index]
                score += abs(time - uav.preferred_time)

            # SE AGREGA EL UAV ACTUAL AL TIEMPO DE LLEGADA.
            arrival_order.append(uav)

        # SE RETORNA UN DICCIONARIO QUE CONTIENE LA SOLUCIÓN, EL PUNTAJE Y EL TIEMPO TOTAL.
        return {"arrival_order": [uav.index for uav in arrival_order], "score": score, "time": time}

    # ALGORITMO GREEDY ESTOCASTICO.
    def stochastic_greedy(self) -> dict:
        # ORDENA TODOS LOS UAVS, EN BASE SUS TIEMPOS TEMPRANOS DE LLEGADA.
        # ALMACENANDOLOS EN UN DICCIONARIO QUE TENDRÁ LOS PESOS DE CADA UAV.
        # MIENTRAS MAS TEMPRANO LLEGUE EL UAV MAYOR SERÁ SU PESO/PROBABILIDAD.
        uavs = {len(self.uavs) - i: uav for i, uav in enumerate(sorted(self.uavs.copy(), key=lambda uav: uav.early_time))}
        # SE INICIALIZA UNA LISTA VACÍA QUE REPRESENTARÁ LA SOLUCIÓN.
        arrival_order = list()
        # SE INICIALIZA EL TIEMPO Y PUNTAJE EN 0.
        time = 0
        score = 0

        # SE RECORRE CADA UAV.
        for i in range(self.n_uavs):
            # DEL DICCIONARIO SE EXTRAEN TODOS LOS PESOS EXISTENTES EN EL DICCIONARIO.
            weights = list(uavs.keys())
            # SE ESCOGE UN UAV EN BASE A LA DISTRIBUCIÓN DE PESOS/PROBABILIDAD IMPUESTA.
            random_index = random.choices(weights, weights=weights, k=1)[0]
            uav = uavs[random_index]

            # EL TIEMPO TOTAL, INICIARÁ COMO EL TIEMPO TEMPRANO DE LLEGADA DEL PRIMER UAV EN ATERRIZAR.
            if i == 0:
                time += uav.early_time
            # PARA EL RESTO DE ITERACIONES, EL TIEMPO AUMENTARÁ COMO LOS TIEMPOS DE SEPARACIÓN DEL UAV ACTUAL CON EL ANTERIOR UAV EN ATERRIZAR.
            # EL PUNTAJE SERÁ LA RESTA ABSOLUTA ENTRE EL TIEMPO TOTAL Y EL TIEMPO PREFERENTE DE LLEGADA DEL UAV ACTUAL.
            else:
                time += uav.separation_time[arrival_order[-1].index]
                score += abs(time - uav.preferred_time)

            # SE AGREGA EL UAV ACTUAL AL TIEMPO DE LLEGADA.
            arrival_order.append(uav)
            # SE BORRA EL UAV ACTUAL DEL DICCIONARIO.
            uavs.pop(random_index, None)

        # SE RETORNA UN DICCIONARIO QUE CONTIENE LA SOLUCIÓN, EL PUNTAJE Y EL TIEMPO TOTAL.
        return {"arrival_order": [uav.index for uav in arrival_order], "score": score, "time": time}

    # ALGORITMO HILL CLIMBING ALGUNA-MEJORA
    def hill_climbing_first_improvement(self, initial_solution:list, iterations:int) -> tuple[dict,list]:
        # SE CALCULA EL PUNTAJE Y TIEMPO DE LA SOLUCIÓN INICIAL ENTREGADA, DENOMINANDOLOS COMO LOS MEJORES HASTA EL MOMENTO.
        best_score, best_time = self.objective_function_value(initial_solution)
        # SE COPIA LA SOLUCIÓN INICIAL Y SE DEJA COMO LA MEJOR HASTA EL MOMENTO.
        best_solution = initial_solution.copy()
        # SE INICIALIZAN SUS MOVIMIENTOS EN 0.
        movements = 0
        # ESTA LISTA SE UTILIZA PARA GENERAR GRÁFICAS DEL RENDIMIENTO DE MEJORA POR CADA MOVIMIENTO.
        graph = [ (movements, best_score) ]

        # SE ITERA UNA CANTIDAD CONFIGURADA DE ITERACIONES.
        for _ in range(iterations):
            # SE ESCOGE UN INDICE DEL 0 AL N_UAVS-1.
            idx = random.randint(0, self.n_uavs - 1)
            # SE GENERAN LOS VECINOS HACIENDO UN SWAP DE LA MEJOR SOLUCIÓN RESPECTO AL INDICE ESCOGIDO DE FORMA ALEATORIA.
            neighbors = self.generate_neighbors(best_solution, idx)
            
            # SE ITERA CADA VECINO
            for neighbor in neighbors:
                # SE CALCULA EL PUNTAJE Y TIEMPO DEL VECINO ITERADO.
                current_score, time = self.objective_function_value(neighbor)

                # SI EL PUNTAJE ES MEJOR QUE EL MEJOR PUNTAJE (MENOR). 
                # ENTONCES LA SOLUCIÓN ACTUAL PASA A SER LA MEJOR SOLUCIÓN.
                if current_score < best_score:
                    best_score = current_score
                    best_solution = neighbor
                    best_time = time
                    movements += 1
                    graph.append( (movements, best_score) )
                    # SE ROMPE EL CICLO YA QUE ENCONTRÓ LA PRIMERA MEJORA DEL VECINDARIO.
                    break  

        # SE RETORNA UN DICCIONARIO QUE CONTIENE LA SOLUCIÓN, EL PUNTAJE, EL TIEMPO TOTAL, Y SUS MOVIMIENTOS REALIZADOS. 
        # ADEMÁS SE RETORNA EL GRÁFICO DE MOVIMIENTOS REALIZADOS.
        return {"arrival_order": best_solution, "score": best_score, "time": best_time, "movements": movements}, graph

    # ALGORITMO HILL CLIMBING ALGUNA-MEJORA
    def hill_climbing_best_improvement(self, initial_solution:list, iterations:int) -> tuple[dict, list]:
        # SE CALCULA EL PUNTAJE Y TIEMPO DE LA SOLUCIÓN INICIAL ENTREGADA, DENOMINANDOLOS COMO LOS MEJORES HASTA EL MOMENTO.
        best_score, best_time = self.objective_function_value(initial_solution)
        # SE COPIA LA SOLUCIÓN INICIAL Y SE DEJA COMO LA MEJOR HASTA EL MOMENTO.
        best_solution = initial_solution.copy()
        # SE INICIALIZAN SUS MOVIMIENTOS EN 0.
        movements = 0
        # ESTA LISTA SE UTILIZA PARA GENERAR GRÁFICAS DEL RENDIMIENTO DE MEJORA POR CADA MOVIMIENTO.
        graph = [ (movements, best_score) ]

        # SE ITERA UNA CANTIDAD CONFIGURADA DE ITERACIONES.
        for _ in range(iterations):
            # SE ESCOGE UN INDICE DEL 0 AL N_UAVS-1.
            idx = random.randint(0, self.n_uavs - 1)
            # SE GENERAN LOS VECINOS HACIENDO UN SWAP DE LA MEJOR SOLUCIÓN RESPECTO AL INDICE ESCOGIDO DE FORMA ALEATORIA.
            neighbors = self.generate_neighbors(best_solution, idx)

            # SE ITERA CADA VECINO
            for neighbor in neighbors:
                # SE CALCULA EL PUNTAJE Y TIEMPO DEL VECINO ITERADO.
                current_score, time = self.objective_function_value(neighbor)

                # SI EL PUNTAJE ES MEJOR QUE EL MEJOR PUNTAJE (MENOR). 
                # ENTONCES LA SOLUCIÓN ACTUAL PASA A SER LA MEJOR SOLUCIÓN.
                # EN ESTE CASO SE RECORRE POR COMPLETO EL VECINDARIO GENERADO PARA BUSCAR EL MEJOR GENERADO.
                if current_score < best_score:
                    best_solution = neighbor
                    best_score = current_score
                    best_time = time
                    movements += 1
                    graph.append( (movements, best_score) )

        # SE RETORNA UN DICCIONARIO QUE CONTIENE LA SOLUCIÓN, EL PUNTAJE, EL TIEMPO TOTAL, Y SUS MOVIMIENTOS REALIZADOS. 
        # ADEMÁS SE RETORNA EL GRÁFICO DE MOVIMIENTOS REALIZADOS.
        return {"arrival_order": best_solution, "score": best_score, "time": best_time, "movements": movements}, graph

    # ALGORITMO HILL CLIMBING ALGUNA-MEJORA
    def tabu_search(self, initial_solution:list, iterations:int, tabu_list_max_len:int) -> tuple[dict, list]:
        # SE CALCULA EL PUNTAJE Y TIEMPO DE LA SOLUCIÓN INICIAL ENTREGADA, DENOMINANDOLOS COMO LOS MEJORES HASTA EL MOMENTO.
        best_score, best_time = self.objective_function_value(initial_solution)
        # SE COPIA LA SOLUCIÓN INICIAL Y SE DEJA COMO LA MEJOR HASTA EL MOMENTO.
        best_solution = initial_solution.copy()
        # SE INICIALIZAN SUS MOVIMIENTOS EN 0.
        movements = 0
        # SE INICIALIZA UNA LISTA TABÚ VACÍA.
        tabu_list = list()
        # ESTA LISTA SE UTILIZA PARA GENERAR GRÁFICAS DEL RENDIMIENTO DE MEJORA POR CADA MOVIMIENTO.
        graph = [ (movements, best_score) ]

        # SE ITERA UNA CANTIDAD CONFIGURADA DE ITERACIONES.
        for _ in range(iterations):
            # SE ESCOGE UN INDICE DEL 0 AL N_UAVS-1.
            idx = random.randint(0, self.n_uavs - 1)
            # SE GENERAN LOS VECINOS HACIENDO UN SWAP DE LA MEJOR SOLUCIÓN RESPECTO AL INDICE ESCOGIDO DE FORMA ALEATORIA.
            neighbors = self.generate_neighbors(list(best_solution), idx)

            # SE ALMACENA EN UN DICCIONARIO EL DICCIONARIO DE VECINOS.
            # TENIENDO LA SOLUCIÓN COMO LLAVE Y SU PUNTAJE COMO VALOR.
            neighbors_dict = dict()
            for neighbor in neighbors:
                current_score, time = self.objective_function_value(neighbor)
                neighbors_dict[tuple(neighbor)] = current_score

            # SE ORDENA DE MENOS A MAYOR EN BASE A LOS PUNTAJES PARA OBTENER EL MEJOR VALOR DEL VECINDARIO.
            sorted_dict = dict(sorted(neighbors_dict.items(), key=lambda x: x[1]))

            # SE RECORRE CADA VECINO DEL DICCIONARIO ORDENADO.
            for k in sorted_dict:
                # SI EL VECINO NO ESTÁ DENTRO DE LA LISTA TABÚ, ENTONCES PODEMOS REALIZAR EL MOVIMIENTO PARA ESTA SOLUCIÓN.
                # EN CASO DE QUE NO, SE ITERA AL SIGUIENTE VECINO.
                if k not in tabu_list:
                    current_solution = k
                    # SI LA LISTA TABÚ SE LLENA, ENTONCES EMPIEZA A ELIMINAR SOLUCIONES USANDO LA PRIORIDAD FIFO.
                    if len(tabu_list) == tabu_list_max_len:
                        tabu_list.pop(0)
                    # SI LA LISTA NO ESTÁ LLENA, ENTONCES SE AÑADE UNA SOLUCIÓN A ESTA.
                    tabu_list.append(k)
                    # SI SE ENCUENTRA UN VECINO QUE NO HAYA ESTADO EN LA LISTA TABÚ, ENTONCES PARAMOS LA BUSQUEDA E ITERAMOS.
                    break

            # SE CALCULA EL PUNTAJE Y TIEMPO DE LA NUEVA SOLUCIÓN ACTUAL.
            current_solution_score, current_solution_time = self.objective_function_value(current_solution)

            # SI EL PUNTAJE ES MEJOR QUE EL MEJOR PUNTAJE (MENOR). 
            # ENTONCES LA SOLUCIÓN ACTUAL PASA A SER LA MEJOR SOLUCIÓN.
            if current_solution_score < best_score:
                best_solution = current_solution
                best_score = current_solution_score
                best_time = current_solution_time
                movements += 1
                graph.append( (movements, best_score) )

        # SE RETORNA UN DICCIONARIO QUE CONTIENE LA SOLUCIÓN, EL PUNTAJE, EL TIEMPO TOTAL, Y SUS MOVIMIENTOS REALIZADOS. 
        # ADEMÁS SE RETORNA EL GRÁFICO DE MOVIMIENTOS REALIZADOS.
        return {"arrival_order": best_solution, "score": best_score, "time": best_time, "movements": movements}, graph

# FUNCIÓN QUE SIRVE SOLAMENTE PARA GRAFICAR LA ACTUALIZACIÓN DE PUNTAJES RESPECTO A CADA MOVIMIENTO REALIZADO POR EL ALGORITMO.
def plot_movements(graph:list, algorith_name:str):
    x = [item[0] for item in graph]
    y = [item[1] for item in graph]

    color_map = LinearSegmentedColormap.from_list('ColorMap', ['red', 'yellow', 'green'])
    fig, ax = plt.subplots(figsize=(12, 6))

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

# FUNCIÓN QUE EJECUTA LOS ALGORITMOS Y PERMITE EXTRAER LOS RESULTADOS SEGÚN SE PIDEN EN EL PROBLEMA DE LA TAREA.
def excute_all_algorithms(path:str, iterations:int, tabu_list_len:int):
    # SE INICIALIZA EL ALGORITMO DE ACUERDO AL ARCHIVO TXT QUE SE LE ENTREGUE.
    problem = Algorithms(path)
    # SE INICIALIZA UN DICCIONARIO QUE ALMACENARÁ EL NOMBRE DEL ALGORITMO Y SUS PUNTAJES OBTENIDOS.
    # SERÁN 2 PUNTAJES; DEPENDIENDO SI SU SOLUCIÓN INICIAL ES CON EL GREEDY DETERMINISTA O ESTOCASTICO.
    score_dict = dict()

    # EJECUCIÓN DEL GREEDY DETERMINISTA.
    deterministic_greedy = problem.deterministic_greedy()
    print("[1] GREEDY DETERMINISTA")
    print(f"Solución: {deterministic_greedy['arrival_order']}\nMejor Puntaje: {deterministic_greedy['score']}\nTiempo: {deterministic_greedy['time']}\n")
    score_dict["Greedy"] = [deterministic_greedy['score']]

    # 5 EJECUCIONES DEL GREEDY ESTOCASTICO.
    stochastic_greedys = sorted([problem.stochastic_greedy() for _ in range(5)], key=lambda sg: sg["score"])
    for index,solution in enumerate(stochastic_greedys):
        print(f"[{index+1}] GREEDY ESTOCASTICO")
        print(f"Solución: {solution['arrival_order']}\nMejor Puntaje: {solution['score']}\nTiempo: {solution['time']}\n")
    # PARA ANALISIS SE ESCOGE LA MEJOR PUNTUACIÓN OBTENIDA.
    score_dict["Greedy"].append( stochastic_greedys[0]["score"] )

    # EJECUCIÓN DE LOS ALGORIMOS HILL CLIMBING ALGUNA-MEJORA Y MEJOR-MEJORA, Y TABÚ SEARCH QUE COMIENZAN CON LA SOLUCIÓN INICIAL OBTENIDA DEL GREEDY DETERMINISTA.
    print("[O] SOLUCIÓN INICIAL - GREEDY DETERMINISTA")
    initial_solution = deterministic_greedy["arrival_order"]

    hill_climbing_first_improvement, hill_climbing_first_improvement_plot = problem.hill_climbing_first_improvement(initial_solution, iterations)
    plot_movements(hill_climbing_first_improvement_plot, "Hill Climbing Alguna-Mejora - Greedy Determinista")
    print("[1] HILL CLIMBING ALGUNA-MEJORA - GREEDY DETERMINISTA")
    print(f"Solución: {hill_climbing_first_improvement['arrival_order']}\nMejor Puntaje: {hill_climbing_first_improvement['score']}\nTiempo: {hill_climbing_first_improvement['time']}\nMovimientos: {hill_climbing_first_improvement['movements']}\n")
    score_dict["HC AM"] = [hill_climbing_first_improvement['score']]

    hill_climbing_best_improvement, hill_climbing_best_improvement_plot = problem.hill_climbing_best_improvement(initial_solution, iterations)
    plot_movements(hill_climbing_best_improvement_plot, "Hill Climbing Mejor-Mejora - Greedy Determinista")
    print("[1] HILL CLIMBING MEJOR-MEJORA - GREEDY DETERMINISTA")
    print(f"Solución: {hill_climbing_best_improvement['arrival_order']}\nMejor Puntaje: {hill_climbing_best_improvement['score']}\nTiempo: {hill_climbing_best_improvement['time']}\nMovimientos: {hill_climbing_best_improvement['movements']}\n")
    score_dict["HC MM"] = [hill_climbing_best_improvement['score']]

    tabu_search, tabu_search_plot = problem.tabu_search(initial_solution, iterations, tabu_list_len)
    plot_movements(tabu_search_plot, "Búsqueda Tabú - Greedy Determinista")
    print("[1] BÚSQUEDA TABÚ - GREEDY DETERMINISTA")
    print(f"Solución: {tabu_search['arrival_order']}\nMejor Puntaje: {tabu_search['score']}\nTiempo: {tabu_search['time']}\nMovimientos: {tabu_search['movements']}\n")
    score_dict["TS"] = [tabu_search['score']]


    # EJECUCIÓN DE LOS ALGORIMOS HILL CLIMBING ALGUNA-MEJORA Y MEJOR-MEJORA, Y TABÚ SEARCH QUE COMIENZAN CON LA SOLUCIÓN INICIAL OBTENIDA DEL GREEDY ESTOCASTICO.
    print("[O] SOLUCIÓN INICIAL - GREEDY ESTOCASTICO")
    initial_solution = stochastic_greedys[0]["arrival_order"]

    hill_climbing_first_improvement, hill_climbing_first_improvement_plot = problem.hill_climbing_first_improvement(initial_solution, iterations)
    plot_movements(hill_climbing_first_improvement_plot, "Hill Climbing Alguna-Mejora - Greedy Estocastico")
    print("[1] HILL CLIMBING ALGUNA-MEJORA - GREEDY ESTOCASTICO")
    print(f"Solución: {hill_climbing_first_improvement['arrival_order']}\nMejor Puntaje: {hill_climbing_first_improvement['score']}\nTiempo: {hill_climbing_first_improvement['time']}\nMovimientos: {hill_climbing_first_improvement['movements']}\n")
    score_dict["HC AM"].append( hill_climbing_first_improvement['score'] )

    hill_climbing_best_improvement, hill_climbing_best_improvement_plot = problem.hill_climbing_best_improvement(initial_solution, iterations)
    plot_movements(hill_climbing_best_improvement_plot, "Hill Climbing Mejor-Mejora - Greedy Estocastico")
    print("[1] HILL CLIMBING MEJOR-MEJORA - GREEDY ESTOCASTICO")
    print(f"Solución: {hill_climbing_best_improvement['arrival_order']}\nMejor Puntaje: {hill_climbing_best_improvement['score']}\nTiempo: {hill_climbing_best_improvement['time']}\nMovimientos: {hill_climbing_best_improvement['movements']}\n")
    score_dict["HC MM"].append( hill_climbing_best_improvement['score'] )

    tabu_search, tabu_search_plot = problem.tabu_search(initial_solution, iterations, tabu_list_len)
    plot_movements(tabu_search_plot, "Búsqueda Tabú - Greedy Estocastico")
    print("[1] BÚSQUEDA TABÚ - GREEDY ESTOCASTICO")
    print(f"Solución: {tabu_search['arrival_order']}\nMejor Puntaje: {tabu_search['score']}\nTiempo: {tabu_search['time']}\nMovimientos: {tabu_search['movements']}\n")
    score_dict["TS"].append( tabu_search['score'] )

    # FINALMENTE SE GRAFICA EL PUNTAJE DE TODOS LOS ALGORITMOS PARA SU POSTERIOR ANALISIS.
    algoritmos_unicos = list(score_dict.keys())

    num_grupos = len(algoritmos_unicos)
    ancho_barras = 0.35

    fig, ax = plt.subplots()

    posiciones_barras_gd = [i - ancho_barras / 2 for i, _ in enumerate(algoritmos_unicos)]
    posiciones_barras_ge = [i + ancho_barras / 2 for i, _ in enumerate(algoritmos_unicos)]

    barras_gd = ax.bar(posiciones_barras_gd, [score_dict[algo][0] for algo in algoritmos_unicos], ancho_barras, label="GD")
    barras_ge = ax.bar(posiciones_barras_ge, [score_dict[algo][1] for algo in algoritmos_unicos], ancho_barras, label="GE")

    ax.set_xlabel("Algoritmos")
    ax.set_ylabel("Puntajes")
    ax.set_title("Puntajes por algoritmo y versión")
    ax.set_xticks(np.arange(num_grupos))
    ax.set_xticklabels(algoritmos_unicos)
    ax.legend()

    for i, algo in enumerate(algoritmos_unicos):
        ax.text(posiciones_barras_gd[i], score_dict[algo][0] + 1, str(score_dict[algo][0]), ha='center', va='bottom')
        ax.text(posiciones_barras_ge[i], score_dict[algo][1] + 1, str(score_dict[algo][1]), ha='center', va='bottom')

    plt.show()

# METODO MAIN.
if __name__ == "__main__":
    # PARAMETROS CONFIGURABLES
    iterations = 10000
    tabu_list_max_len = 1000

    # DESCOMENTAR DEPENDIENDO DEL ARCHIVO TXT QUE DESEE UTILIZAR.
    print("[*] FILE NAME: TITAN\n"); excute_all_algorithms("./data/t2_Titan.txt", iterations, tabu_list_max_len)
    # print("[*] FILE NAME: EUROPA\n"); excute_all_algorithms("./data/t2_Europa.txt", iterations, tabu_list_max_len)
    # print("[*] FILE NAME: DEIMOS\n"); excute_all_algorithms("./data/t2_Deimos.txt", iterations, tabu_list_max_len)