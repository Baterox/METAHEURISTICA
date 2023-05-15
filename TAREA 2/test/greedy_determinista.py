from obj.UAV import UAV

class GreedyDeterminista:
    def __init__(self, archivo:str):
        file = open(archivo, "r")

        self.n_uavs = int(file.readline())
        self.uavs = list()
        
        if("Titan" in archivo):
            nsep = 2
        else:
            nsep = 4

        for i in range(self.n_uavs):
            tiempo_temprano, tiempo_preferente, tiempo_tarde = [int(num) for num in file.readline().split()]
            self.uavs.append(UAV(i, tiempo_temprano, tiempo_preferente, tiempo_tarde))
            for _ in range(nsep):
                self.uavs[i].tiempo_separacion += [int(num) for num in file.readline().split()]

    def print_uavs(self):
        print("-"*80)
        for uav in self.uavs:
            print(f"UAV {uav.index}:\t{uav.tiempo_temprano} {uav.tiempo_preferente} {uav.tiempo_tarde} \n\t{uav.tiempo_separacion}")
            print("-"*80)

    def solve(self):
        UAVS = sorted(self.uavs, key=lambda uav: uav.tiempo_temprano)
        orden_llegada = list()
        tiempo = 0
        puntaje = 0

        for i, uav in enumerate(UAVS):
            if i == 0:
                tiempo += uav.tiempo_temprano
                print(f"[+] Atterriza UAV {uav.index} - {tiempo}/{uav.tiempo_preferente}")
                orden_llegada.append(uav)
                continue

            # tiempo += orden_llegada[-1].tiempo_separacion[uav.index]
            tiempo += uav.tiempo_separacion[orden_llegada[-1].index]
            if tiempo <= uav.tiempo_preferente:
                print(f"[+] Atterriza UAV {uav.index} - {tiempo}/{uav.tiempo_preferente} ")
            else:
                print(f"[-] Atterriza UAV Tarde {uav.index} - {tiempo}/{uav.tiempo_preferente}")
                puntaje += tiempo - uav.tiempo_preferente
                
            orden_llegada.append(uav)

        print(f"Puntaje: {puntaje}")
        print(f"Orden De Llegada: {[uav.index for uav in UAVS]}")

if __name__ == "__main__":
    problem_titan = GreedyDeterminista("./data/t2_Titan.txt")
    # problem_titan.print_uavs()
    problem_titan.solve()