import random
from copy import deepcopy

class Pedido:
    def __init__(self, id, tiempo_procesamiento):
        self.id = id
        self.tiempo_procesamiento = tiempo_procesamiento
        self.confirmado = False

    def __repr__(self):
        return f"\nPedido(id={self.id}, tiempo={self.tiempo_procesamiento}, confirmado={self.confirmado})"

class Vehiculo:
    def __init__(self, id):
        self.id = id
        self.posicion = 0
        self.capacidad = 100  # Capacidad hipotética
        self.tiempo_viaje = 0

    def __repr__(self):
        return f"\nVehiculo(id={self.id}, posicion={self.posicion}, capacidad={self.capacidad}, tiempo_viaje={self.tiempo_viaje})"

class VRP:
    def __init__(self, pedidos, vehiculos):
        self.pedidos = {p.id: p for p in pedidos}
        self.vehiculos = {v.id: v for v in vehiculos}
        self.T = 480  # Ejemplo: 8 horas de trabajo en minutos
        self.nst = 8  # 8 secciones temporales
        self.Tst = self.T / self.nst
        self.no_servidos = list(pedidos)

    def solucion_inicial(self):
        solucion = list(self.pedidos.values())
        random.shuffle(solucion)
        return solucion

    def vns(self, solucion_actual):
        mejor_solucion = deepcopy(solucion_actual)
        mejor_costo = self.evaluar_solucion(mejor_solucion)
        k = 0
        max_k = 10
        iter_sin_mejora = 0
        max_iter_sin_mejora = 50

        while k < max_k and iter_sin_mejora < max_iter_sin_mejora:
            nueva_solucion = self.perturbar_solucion(deepcopy(mejor_solucion), k)
            nueva_costo = self.evaluar_solucion(nueva_solucion)
            if nueva_costo < mejor_costo:
                mejor_solucion = nueva_solucion
                mejor_costo = nueva_costo
                k = 0
                iter_sin_mejora = 0
            else:
                k += 1
                iter_sin_mejora += 1

        return mejor_solucion

    def perturbar_solucion(self, solucion, nivel_de_perturbacion):
        for _ in range(nivel_de_perturbacion + 1):
            i, j = random.sample(range(len(solucion)), 2)
            solucion[i], solucion[j] = solucion[j], solucion[i]
        return solucion

    def evaluar_solucion(self, solucion):
        return sum(not p.confirmado for p in solucion)

def controlador_de_eventos(vrp):
    Tstep = 0
    while any(not p.confirmado for p in vrp.no_servidos):
        print(f"---- Tstep: {Tstep} ----")
        problemas_parciales = [p for p in vrp.no_servidos if p.tiempo_procesamiento <= Tstep + vrp.Tst]
        solucion = vrp.solucion_inicial()
        solucion = vrp.vns(solucion)

        print("Solución propuesta:", solucion, "\n")
        
        confirmados = [p for p in problemas_parciales if Tstep <= p.tiempo_procesamiento < Tstep + vrp.Tst]
        for p in confirmados:
            p.confirmado = True
            vrp.no_servidos.remove(p)

        print("Pedidos confirmados:", confirmados, "\n")
        print("Vehículos:", list(vrp.vehiculos.values()), "\n")

        Tstep += vrp.Tst

        for v in vrp.vehiculos.values():
            v.tiempo_viaje += 10  # Simulación del incremento de tiempo de viaje

# Simulación inicial
pedidos = [Pedido(i, random.randint(0, 480)) for i in range(10)]
vehiculos = [Vehiculo(i) for i in range(3)]
vrp = VRP(pedidos, vehiculos)

controlador_de_eventos(vrp)
