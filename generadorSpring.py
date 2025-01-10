from generadorGrafos import Grafo
from generadorModelos import *
import numpy, pygame

modelo = modeloMalla(3,3)
print(modelo)
# Parámetros del algoritmo
ca = 0.05  # Constante de atracción
cr = 50  # Constante de repulsión
friccion = 0.97  # Fricción para estabilizar el sistema
maxVelocidad = 5  # Velocidad máxima
minDistancia = 5  # Velocidad mínima

# Nodos y aristas del modelo
nodos = modelo.nodos
aristas = modelo.aristas
velocidades = {nodo: numpy.array([0, 0]) for nodo in nodos}
velMATH = {i: [0,0] for i in nodos}

def obtenerDistancia(modelo, nodo1, nodo2):
    """
    Calcula la distancia entre dos nodos
    """
    nodo1 = modelo.obtenerPosicion(int(nodo1))
    nodo2 = modelo.obtenerPosicion(int(nodo2))
    distancia = numpy.linalg.norm(nodo1 - nodo2)
    dx = abs(nodo2[0] - nodo1[0])
    dy = abs(nodo2[1] - nodo1[1])
    return distancia, dx, dy

def fzaAtraccion(modelo, nodo1, nodo2):
    """
    Calcula la fuerza de atracción entre dos nodos 
    conectados por una arista
    """
    distancia = obtenerDistancia(modelo, nodo1, nodo2)[0]
    fuerza = ca * numpy.log(distancia + 1)
    #print(f"N1: {nodo1}, N2: {nodo2} Fza atraccion: {fuerza}")
    return fuerza

def fzaRepulsion(modelo, nodo1, nodo2):
    """
    Calcula la fuerza de repulsión entre dos nodos
    """
    distancia = obtenerDistancia(modelo, nodo1, nodo2)[0]
    fuerza = cr / (distancia ** 2)
    #print(f"N1: {nodo1}, N2: {nodo2} Fza repulsiva: {fuerza}")
    return fuerza

def Spring(modelo):
    """
    Método Spring para la visualización de grafos
    """
    run = True
    while run:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False

        fuerzas = {int(nodo): numpy.array([0, 0]) for nodo in nodos}
        fzsMATH = {i: [0,0] for i in nodos}
            
        # Calcular fuerzas de atracción
        for i in aristas:
            n1, n2 = modelo.nodoVecino(i)
            distancia, dx, dy = obtenerDistancia(modelo, n1, n2)
            if distancia > 0:
                f = fzaAtraccion(modelo, n1, n2)
                fuerzas[int(n1)] = numpy.array([(fuerzas.get(int(n1))[0] + f * dx) / distancia,\
                                                (fuerzas.get(int(n1))[1] + f * dy) / distancia])
                fuerzas[int(n2)] = numpy.array([(fuerzas.get(int(n2))[0] - f * dx) / distancia,\
                                                (fuerzas.get(int(n2))[1] - f * dy) / distancia])
                print(f"\nFuerzas NUMPY: {fuerzas.get(int(n1))}, {fuerzas.get(int(n2))}")
                fzsMATH[int(n1)][0] += f * dx /distancia
                fzsMATH[int(n1)][1] += f * dy /distancia
                fzsMATH[int(n2)][0] -= f * dx /distancia
                fzsMATH[int(n2)][1] -= f * dy /distancia
                print(f"Fuerzas MATH: {fzsMATH.get(int(n1))}, {fzsMATH.get(int(n2))}")
            
        # Calcular fuerzas de repulsión
        print("REPULSION")
        for n1 in nodos:
            for n2 in nodos:
                if n1 != n2:
                    distancia, dx, dy = obtenerDistancia(modelo, n1, n2)
                    if distancia > minDistancia:
                        f = fzaRepulsion(modelo, n1, n2)
                        fuerzas[int(n1)] = numpy.array([(fuerzas.get(int(n1))[0] - f * dx) / distancia,\
                                                        (fuerzas.get(int(n1))[1] - f * dy) / distancia])
                        fzsMATH[int(n1)][0] -= f * dx /distancia
                        fzsMATH[int(n1)][1] -= f * dy /distancia
                        print(f"\nFuerzas NUMPY: {fuerzas.get(int(n1))}")
                        print(f"Fuerzas MATH: {fzsMATH.get(int(n1))}")


        # Actualizar posiciones
        for nodo in nodos:
            """velocidades[nodo] = numpy.array([(max(-maxVelocidad, min(maxVelocidad, (velocidades.get(nodo)[0] + fuerzas.get(int(nodo))[0])*friccion))),\
                                            (max(-maxVelocidad, min(maxVelocidad, (velocidades.get(nodo)[1] + fuerzas.get(int(nodo))[1])*friccion)))])
            modelo.actualizarPosicion(int(nodo), velocidades.get(nodo))"""

            velMATH[nodo][0] = max(-maxVelocidad, min(maxVelocidad, (velMATH[int(nodo)][0] + fzsMATH[int(nodo)][0])*friccion))
            velMATH[nodo][1] = max(-maxVelocidad, min(maxVelocidad, (velMATH[int(nodo)][1] + fzsMATH[int(nodo)][1])*friccion))
            velMATH[nodo] = numpy.array(velMATH.get(nodo))
            modelo.actualizarPosicion(int(nodo), velMATH.get(nodo))
            
        # Dibujar en pantalla
        pantalla.fill((255, 255, 255))
        for i in aristas:
            n1, n2 = modelo.nodoVecino(i)
            n1 = modelo.obtenerPosicion(int(n1))
            n1 = numpy.array([int(n1[0]),int(n1[1])])

            n2 = modelo.obtenerPosicion(int(n2))  
            n2 = numpy.array([int(n2[0]),int(n2[1])])      
            pygame.draw.line(pantalla, (200,200,200), n1, n2, 2)

        for i in nodos:
            n = modelo.obtenerPosicion(i)
            n = numpy.array([int(n[0]), int(n[1])])
            pygame.draw.circle(pantalla, (50, 150, 250), n, 5)
                
        pygame.display.flip()
        reloj.tick(FPS)

    return True #modelo.posicion


# Inicializar pygame
pygame.init()
# Parámetros de la pantalla
tamanioPantalla = (800, 800)  # Tamaño de la pantalla
FPS = 30
pantalla = pygame.display.set_mode(tamanioPantalla)
pygame.display.set_caption("Algoritmo de Resortes")
font = pygame.font.SysFont(None, 24)
reloj = pygame.time.Clock()

for i in nodos:
    x = modelo.obtenerPosicion(int(i))
    print(f"Posición de {i}: {x}")

Spring(modelo)

pygame.quit()
