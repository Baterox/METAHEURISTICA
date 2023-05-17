# CLASE UAV
# CONTIENE LOS PARAMETROS: TIEMPO TEMPRANO DE LLEGADA, TIEMPO PREFERENTE DE LLEGADA Y TIEMPO TARDE DE LLEGADA.
# ADEMÁS SE INICIALIZA CON UNA LISTA VACÍA QUE TENDRÁ LOS TIEMPOS DE SEPARACIÓN RESPECTO A LOS DEMÁS UAVS.
class UAV:
    def __init__(self, index:int, early_time:int, preferred_time:int, late_time:int):
        self.index = index
        self.early_time = early_time
        self.preferred_time = preferred_time
        self.late_time = late_time
        self.separation_time = list()