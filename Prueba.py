import pygame, math, random
from generadorModelos import *
from generadorGrafos import Grafo

# Configuración de pantalla
ancho, alto = 1900, 1000
radioNodo = 4
colorArista = (200, 200, 200)
colorNodo = (50, 150, 250)
colorFondo = (30, 30, 30)
reloj = pygame.time.Clock()
FPS = 240

# Algoritmo de resortes
def fzaAtractiva(d, k):
    """
    Calcula la fuerza de atracción entre dos nodos 
    conectados por una arista
    """
    return (d ** 2) / k

def fzaRepulsiva(d, k):
    """
    Calcula la fuerza de repulsión entre dos nodos
    """
    return k ** 2 / d if d > 0 else k ** 2

# Inicializar posiciones y fuerzas
def posicionesIniciales(graph, ancho, alto):
    """
    Obtiene posiciones iniciales aleatorias para los nodos
    """
    posiciones = {nodo: (random.randint(50, ancho - 50), random.randint(50, alto - 50))\
                  for nodo in graph["nodes"]}
    return posiciones

def Spring(graph, posiciones, ancho, alto, screen=None):
    """
    Método Spring para la visualización de grafos
    """
    #250*230
    k = math.sqrt((250 * 230) / (len(graph["nodes"])/ 2))/2  # Constante de distancia óptima
    # Calcular fuerzas repulsivas
    fuerzas = {nodo: [0, 0] for nodo in graph["nodes"]}
    for n1 in graph["nodes"]:
        for n2 in graph["nodes"]:
            if n1 != n2:
                x1, y1 = posiciones[n1]
                x2, y2 = posiciones[n2]
                dx, dy = x2 - x1, y2 - y1
                distancia = math.sqrt(dx**2 + dy**2)
                fuerza = fzaRepulsiva(distancia, k)
                angulo = math.atan2(dy, dx)
                fuerzas[n1][0] -= math.cos(angulo) * fuerza
                fuerzas[n1][1] -= math.sin(angulo) * fuerza

    # Calcular fuerzas atractivas
    for e in graph["edges"]:
        n1, n2 = e
        x1, y1 = posiciones[n1]
        x2, y2 = posiciones[n2]
        dx, dy = x2 - x1, y2 - y1
        distancia = math.sqrt(dx**2 + dy**2)
        fuerza = fzaAtractiva(distancia, k)
        angulo = math.atan2(dy, dx)
        fuerzas[n1][0] += math.cos(angulo) * fuerza
        fuerzas[n1][1] += math.sin(angulo) * fuerza
        fuerzas[n2][0] -= math.cos(angulo) * fuerza
        fuerzas[n2][1] -= math.sin(angulo) * fuerza

    m = 0.001 # Factor de movimiento
    # Actualizar posiciones
    for n in graph["nodes"]:
        posiciones[n] = (
            min(ancho - 25, max(25, posiciones[n][0] + fuerzas[n][0] * m)),
            min(alto - 25, max(25, posiciones[n][1] + fuerzas[n][1] * m)),
        )
    draw_graph(screen, graph, posiciones)   
    
    return posiciones

# Dibujar grafo con Pygame
def draw_graph(screen, graph, posiciones):
    screen.fill(colorFondo)
    # Dibujar aristas
    for edge in graph["edges"]:
        n1, n2 = edge
        pygame.draw.line(screen, colorArista, posiciones[n1], posiciones[n2], 2)
    # Dibujar nodos
    for node, (x, y) in posiciones.items():
        pygame.draw.circle(screen, colorNodo, (int(x), int(y)), radioNodo)
    pygame.display.flip()
    reloj.tick(FPS)

# Main
def main():
    pygame.init()
    screen = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Visualización de Grafos - Método de Resortes")

    n = 100
    modelo = modeloErdosRenyi(n,int(n*1.5))
    #print(modelo)

    nodes = []
    edges = []
    for i in modelo.nodos.values():
        nodes.append(i)

    for i in modelo.aristas.values():
        e = modelo.nodoVecino(i)
        edges.append(e)

    graph = {
        "nodes": nodes,
        "edges": edges,
    }

    posiciones = posicionesIniciales(graph, ancho, alto)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #draw_graph(screen, graph, posiciones)
        Spring(graph, posiciones, ancho, alto, screen=screen)
    pygame.quit()

if __name__ == "__main__":
    main()

