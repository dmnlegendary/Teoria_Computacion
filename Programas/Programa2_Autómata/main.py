# Diaz Jimenez Jorge Arif 5BM2

import random
import matplotlib.pyplot as plt
import networkx as nx
import time

class Board:
    def __init__(self):
        self.size = 5
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def is_within_bounds(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

class Player:
    def __init__(self, name, start_pos, end_pos):
        self.name = name
        self.position = start_pos  # (x, y)
        self.end_position = end_pos
        self.moves = []

    def move_orthogonal(self, direction, board):
        x, y = self.position

        if direction == 'up' and board.is_within_bounds(x - 1, y):
            self.position = (x - 1, y)
        elif direction == 'down' and board.is_within_bounds(x + 1, y):
            self.position = (x + 1, y)
        elif direction == 'left' and board.is_within_bounds(x, y - 1):
            self.position = (x, y - 1)
        elif direction == 'right' and board.is_within_bounds(x, y + 1):
            self.position = (x, y + 1)
        else:
            print(f"Movimiento '{direction}' inválido para {self.name}.")
        
        self.moves.append(self.position)  # Registrar el movimiento
        return self.position

    def move_diagonal(self, direction, board):
        x, y = self.position

        if direction == 'up-left' and board.is_within_bounds(x - 1, y - 1):
            self.position = (x - 1, y - 1)
        elif direction == 'up-right' and board.is_within_bounds(x - 1, y + 1):
            self.position = (x - 1, y + 1)
        elif direction == 'down-left' and board.is_within_bounds(x + 1, y - 1):
            self.position = (x + 1, y - 1)
        elif direction == 'down-right' and board.is_within_bounds(x + 1, y + 1):
            self.position = (x + 1, y + 1)
        else:
            print(f"Movimiento '{direction}' inválido para {self.name}.")
        
        self.moves.append(self.position)  # Registrar el movimiento
        return self.position

def decide_first_player(players):
    return random.choice(players)

def generate_moves_randomly(max_moves=100):
    directions = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']
    return [random.choice(directions) for _ in range(random.randint(5, max_moves))]

def plot_board(board, players):
    plt.figure(figsize=(6, 6))
    ax = plt.gca()

    # Dibujar el tablero
    for x in range(board.size):
        for y in range(board.size):
            if (x + y) % 2 == 0:
                color = 'lightgray'  # Color claro para casillas blancas
            else:
                color = 'darkgray'   # Color oscuro para casillas negras
            ax.add_patch(plt.Rectangle((y, board.size - 1 - x), 1, 1, color=color))

    # Dibujar las piezas de los jugadores
    for player in players:
        x, y = player.position
        ax.text(y + 0.5, board.size - 1 - x + 0.5, player.name, ha='center', va='center', fontsize=16)

    # Configurar los límites del gráfico
    ax.set_xlim(0, board.size)
    ax.set_ylim(0, board.size)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    # Mostrar el gráfico
    plt.title("Tablero de Ajedrez 5x5")
    plt.grid(False)
    plt.show()

def create_nfa_graph(board, players):
    G = nx.DiGraph()  # Crear un grafo dirigido

    # Crear nodos para cada posición en el tablero
    for x in range(board.size):
        for y in range(board.size):
            G.add_node((x, y))  # Cada posición es un nodo

    # Agregar aristas basadas en movimientos ortogonales y diagonales
    for x in range(board.size):
        for y in range(board.size):
            current_pos = (x, y)
            # Movimientos ortogonales
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_pos = (x + dx, y + dy)
                if board.is_within_bounds(new_pos[0], new_pos[1]):
                    G.add_edge(current_pos, new_pos, label='ortogonal')

            # Movimientos diagonales
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                new_pos = (x + dx, y + dy)
                if board.is_within_bounds(new_pos[0], new_pos[1]):
                    G.add_edge(current_pos, new_pos, label='diagonal')

    # Añadir nodos finales basados en las posiciones de los jugadores
    for player in players:
        G.add_node(player.end_position)

    # Graficar el NFA
    pos = {(x, y): (y, board.size - 1 - x) for x in range(board.size) for y in range(board.size)}
    labels = {(x, y): f"{(x, y)}" for x in range(board.size) for y in range(board.size)}
    
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=500, node_color='lightblue', font_size=8, font_weight='bold', edge_color='gray')

    # Resaltar los nodos finales
    for player in players:
        plt.scatter(*pos[player.end_position], s=400, edgecolor='yellow', facecolor='none', linewidth=2)

    plt.title("NFA Graph - Movimientos en el Tablero")
    plt.grid(False)
    plt.show()

    return G

# Configuración inicial
board = Board()
player1 = Player("Player 1", (0, 0), (4, 4))
player2 = Player("Player 2", (0, 4), (4, 0))
players = [player1, player2]

# Generar movimientos aleatorios para ambos jugadores
moves_player1 = generate_moves_randomly(20)
moves_player2 = generate_moves_randomly(20)

# Ejecutar los movimientos hasta que un jugador alcance su posición final
for move1, move2 in zip(moves_player1, moves_player2):
    # Mover al jugador 1
    player1.move_orthogonal(move1, board) if move1 in ['up', 'down', 'left', 'right'] else player1.move_diagonal(move1, board)
    
    # Mover al jugador 2
    player2.move_orthogonal(move2, board) if move2 in ['up', 'down', 'left', 'right'] else player2.move_diagonal(move2, board)

    # Graficar el tablero después de cada movimiento
    plot_board(board, players)

    # Comprobar si algún jugador ha alcanzado su posición final
    if player1.position == player1.end_position:
        print(f"{player1.name} ha alcanzado la meta!")
        break
    elif player2.position == player2.end_position:
        print(f"{player2.name} ha alcanzado la meta!")
        break

# Graficar el NFA final
nfa_graph = create_nfa_graph(board, players)
