def generar_vecinos(arreglo, indice):
    vecinos_generados = []
    
    # Intercambios hacia adelante
    for i in range(indice + 1, len(arreglo)):
        nuevo_arreglo = arreglo.copy()
        nuevo_arreglo[indice], nuevo_arreglo[i] = nuevo_arreglo[i], nuevo_arreglo[indice]
        vecinos_generados.append(nuevo_arreglo)
    
    # Intercambios hacia atrás
    for i in range(indice - 1, -1, -1):
        nuevo_arreglo = arreglo.copy()
        nuevo_arreglo[indice], nuevo_arreglo[i] = nuevo_arreglo[i], nuevo_arreglo[indice]
        vecinos_generados.append(nuevo_arreglo)
    
    return vecinos_generados

# Ejemplo de uso
arreglo_inicial = [1, 2, 3, 4, 5, 6]
indice_intercambio = 2

vecinos = generar_vecinos(arreglo_inicial, indice_intercambio)
for vecino in vecinos:
    print(vecino)