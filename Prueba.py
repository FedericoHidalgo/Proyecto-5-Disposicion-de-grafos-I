import pygame, math, random
from generadorModelos import *

# Configuración de pantalla
WIDTH, HEIGHT = 1000, 800
NODE_RADIUS = 4
EDGE_COLOR = (200, 200, 200)
NODE_COLOR = (50, 150, 250)
BG_COLOR = (30, 30, 30)
reloj = pygame.time.Clock()
FPS = 60

# Algoritmo de resortes
def attractive_force(d, k):
    return (d ** 2) / k

def repulsive_force(d, k):
    return k ** 2 / d if d > 0 else k ** 2

# Inicializar posiciones y fuerzas
def initialize_positions(graph, width, height):
    positions = {node: (random.randint(50, width - 50), random.randint(50, height - 50))\
                  for node in graph["nodes"]}
    return positions

def spring_layout(graph, positions, width, height, iterations=500, screen=None):
    k = math.sqrt((width * height) / len(graph["nodes"]))  # Constante de distancia óptima
    for _ in range(iterations):
        # Calcular fuerzas repulsivas
        forces = {node: [0, 0] for node in graph["nodes"]}
        for node1 in graph["nodes"]:
            for node2 in graph["nodes"]:
                if node1 != node2:
                    x1, y1 = positions[node1]
                    x2, y2 = positions[node2]
                    dx, dy = x2 - x1, y2 - y1
                    distance = math.sqrt(dx**2 + dy**2)
                    force = repulsive_force(distance, k)
                    angle = math.atan2(dy, dx)
                    forces[node1][0] -= math.cos(angle) * force
                    forces[node1][1] -= math.sin(angle) * force

        # Calcular fuerzas atractivas
        for edge in graph["edges"]:
            node1, node2 = edge
            x1, y1 = positions[node1]
            x2, y2 = positions[node2]
            dx, dy = x2 - x1, y2 - y1
            distance = math.sqrt(dx**2 + dy**2)
            force = attractive_force(distance, k)
            angle = math.atan2(dy, dx)
            forces[node1][0] += math.cos(angle) * force
            forces[node1][1] += math.sin(angle) * force
            forces[node2][0] -= math.cos(angle) * force
            forces[node2][1] -= math.sin(angle) * force

        # Actualizar posiciones
        for node in graph["nodes"]:
            positions[node] = (
                min(width - 50, max(50, positions[node][0] + forces[node][0] * 0.1)),
                min(height - 50, max(50, positions[node][1] + forces[node][1] * 0.1)),
            )
        draw_graph(screen, graph, positions)
    return positions

# Dibujar grafo con Pygame
def draw_graph(screen, graph, positions):
    screen.fill(BG_COLOR)
    # Dibujar aristas
    for edge in graph["edges"]:
        node1, node2 = edge
        pygame.draw.line(screen, EDGE_COLOR, positions[node1], positions[node2], 2)
    # Dibujar nodos
    for node, (x, y) in positions.items():
        pygame.draw.circle(screen, NODE_COLOR, (int(x), int(y)), NODE_RADIUS)
    pygame.display.flip()
    reloj.tick(FPS)

# Main
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Visualización de Grafos - Método de Resortes")

    modelo = modeloMalla(5,5)

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
    
    for arista in graph["edges"]:
        e1, e2 = arista
        print(f"Arista: {e1}, {e2}")

    positions = initialize_positions(graph, WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #draw_graph(screen, graph, positions)
        spring_layout(graph, positions, WIDTH, HEIGHT, screen=screen)
    pygame.quit()

if __name__ == "__main__":
    main()

