import random

def inicializar_solucion(num_vehiculos, num_clientes):
    """ Crea una solución inicial de manera aleatoria. """
    solucion = list(range(num_clientes))
    random.shuffle(solucion)
    return [solucion[i::num_vehiculos] for i in range(num_vehiculos)]

def calcular_costo(solucion):
    """ Calcula el costo ficticio de una solución. """
    return sum(random.randint(1, 10) * len(ruta) for ruta in solucion)

def buscar_local(solucion):
    """ Aplica una heurística de búsqueda local simple a la solución. """
    for ruta in solucion:
        if len(ruta) > 2:
            i, j = sorted(random.sample(range(len(ruta)), 2))
            ruta[i:j] = reversed(ruta[i:j])
    return solucion

def cambiar_vecindario(solucion, k):
    """ Realiza un cambio en el vecindario basado en k. """
    for _ in range(k):
        ruta1, ruta2 = random.sample(solucion, 2)
        if ruta1 and ruta2:
            ruta1[-1], ruta2[0] = ruta2[0], ruta1[-1]
    return solucion

def vns(num_vehiculos, num_clientes, k_max=5, max_iter=50):
    """ Algoritmo VNS para el problema de VRP dinámico. """
    solucion = inicializar_solucion(num_vehiculos, num_clientes)
    costo = calcular_costo(solucion)
    
    for _ in range(max_iter):
        k = 1
        while k <= k_max:
            nueva_solucion = cambiar_vecindario(solucion, k)
            nueva_solucion = buscar_local(nueva_solucion)
            nuevo_costo = calcular_costo(nueva_solucion)
            
            if nuevo_costo < costo:
                solucion, costo = nueva_solucion, nuevo_costo
                k = 1  # Reinicia la búsqueda en el primer vecindario
            else:
                k += 1
    
    return solucion, costo

# Parámetros de simulación
num_vehiculos = 5
num_clientes = 30

solucion_final, costo_final = vns(num_vehiculos, num_clientes)
print("Solución final:", solucion_final)
print("Costo final:", costo_final)
