mi_diccionario = {
    "a": 1,
    "b": 2,
    "c": 3
}

# Imprimir el diccionario original
print("Diccionario original:", mi_diccionario)

# Eliminar un valor del diccionario según su llave
llave_a_eliminar = "b"
valor_eliminado = mi_diccionario.pop(llave_a_eliminar, None)

print("Diccionario después de eliminar la llave:", mi_diccionario)