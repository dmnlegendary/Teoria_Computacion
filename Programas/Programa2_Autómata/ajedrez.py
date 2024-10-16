import pygame
import random
import ast

tablero = [
    ['b', 'r', 'b', 'r'],
    ['r', 'b', 'r', 'b'],
    ['b', 'r', 'b', 'r'],
    ['r', 'b', 'r', 'b']
]

TAMANO_TABLERO = 4
direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def numero_a_coordenada(numero):
    x = (numero - 1) // TAMANO_TABLERO
    y = (numero - 1) % TAMANO_TABLERO
    return (x, y)

def es_valida(x, y):
    return 0 <= x < TAMANO_TABLERO and 0 <= y < TAMANO_TABLERO

def coordenada_a_numero(x, y):
    return x * TAMANO_TABLERO + y + 1

def explorar_ruta(x, y, secuencia, ruta_actual, rutas, casilla_final, todas_rutas, longitud_secuencia):

    if ruta_completa(ruta_actual, longitud_secuencia):
        todas_rutas.append(ruta_actual.copy())
        if not secuencia and ruta_actual[-1] == casilla_final:
            rutas.append(ruta_actual.copy())
        return 

    if not secuencia:
        return

    color_actual = secuencia[0]
    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        if es_valida(nx, ny) and tablero[nx][ny] == color_actual:
            siguiente_casilla=coordenada_a_numero(nx,ny)
            ruta_actual.append(coordenada_a_numero(nx, ny))
            # print("Ruta actual después de agregar nueva casilla:", ruta_actual) # Imprime la ruta después de agregar una nueva casilla
            # print("Avanzando a la casilla: ", siguiente_casilla, "Coordenadas: ", (nx,ny))
            explorar_ruta(nx, ny, secuencia[1:], ruta_actual, rutas, casilla_final, todas_rutas, longitud_secuencia)
            ruta_actual.pop()
            # print("Retrocedeiendo a la casilla: ", ruta_actual[-1] if ruta_actual else "Inicio", "después de explorar", siguiente_casilla)
            # print("Ruta actual después de eliminar última casilla:", ruta_actual)  # Imprime la ruta después de eliminar la última casilla agregada

def ruta_completa(ruta_actual, longitud_secuencia):
    count = 0
    for _ in ruta_actual:
        count += 1
    return count - 1 == longitud_secuencia


def buscar_rutas(secuencia, casilla_inicio, casilla_final):
    rutas = []
    todas_rutas = []
    inicio_x, inicio_y = (casilla_inicio - 1) // TAMANO_TABLERO, (casilla_inicio - 1) % TAMANO_TABLERO
    explorar_ruta(inicio_x, inicio_y, secuencia, [casilla_inicio], rutas, casilla_final, todas_rutas, longitud_secuencia(secuencia))
    return rutas, todas_rutas

def longitud_secuencia(secuencia):
    count = 0
    for _ in secuencia:
        count += 1
    return count

def obtener_secuencia(opcion):
    if opcion == 1:
        return input("Introduce la secuencia para el jugador ('r' para roja, 'b' para negra): ")
    elif opcion == 2:
        longitu_secuencia = random.randint(4,7)
        return ''.join(random.choice(['r', 'b']) for _ in range(longitu_secuencia))
    

def generar_y_buscar_rutas(casilla_inicio, casilla_final, opcion_ingreso):
    rutas_encontradas = []
    todas_las_rutas = []
    secuencia_generada = ""
    intentos = 0

    while not rutas_encontradas:
        secuencia_generada = obtener_secuencia(opcion_ingreso)
        rutas_encontradas, todas_las_rutas = buscar_rutas(secuencia_generada, casilla_inicio, casilla_final)
        intentos += 1
        if intentos > 1:
            print(f"Intento {intentos}: Generando nueva secuencia...")

    return secuencia_generada, rutas_encontradas, todas_las_rutas


opcion_ingreso = int(input("Elige el modo de ingreso de secuencias (1 para manual, 2 para aleatorio): "))
num_jugadores = 2

print("\nJugador 1")
secuencia_jugador1 =obtener_secuencia(opcion_ingreso)
rutas_jugador1, todas_rutas_jugador1 = buscar_rutas(secuencia_jugador1, 1, 16)


while not rutas_jugador1:
    if opcion_ingreso==1:
        print(f"No hay rutas ganadoras para el jugador 1 con la combinación: {secuencia_jugador1}. Dame otra:\n")
        secuencia_jugador1 = obtener_secuencia(opcion_ingreso)  # Corregido aquí
        rutas_jugador1, todas_rutas_jugador1 = buscar_rutas(secuencia_jugador1, 1, 16)
    else:
        print(f"No hay rutas ganadoras para el jugador 1 con la combinación: {secuencia_jugador1}"+ "\nCalculando nueva ruta aleatorea")
        longitu_secuencia = random.randint(4, 7)
        secuencia_jugador1 = ''.join(random.choice(['r', 'b']) for _ in range(longitu_secuencia))
        rutas_jugador1, todas_rutas_jugador1 = buscar_rutas(secuencia_jugador1, 1, 16)

with open("Ajedrez/rutas_jugador1_coordenadas.txt", "w") as archivo:
    for ruta in rutas_jugador1:
        # Convertir los números a coordenadas
        ruta_coordenadas = [numero_a_coordenada(numero) for numero in ruta]
        # Escribir la ruta como string de coordenadas
        archivo.write(str(ruta_coordenadas) + "\n")

with open("Ajedrez/rutas_jugador1.txt", "w") as archivo:
    for ruta in rutas_jugador1:
        archivo.write(' '.join(map(str, ruta)) + "\n")

with open("Ajedrez/todas_rutas_jugador1.txt", "w") as archivo:
    for ruta in todas_rutas_jugador1:
        archivo.write(' '.join(map(str, ruta)) + "\n")
print(f"Jugador 1: Verifica 'rutas_jugador1.txt' para rutas válidas y 'todas_rutas_jugador1.txt' para todas las rutas exploradas que cumplen con el tamaño de la secuencia.\n")



if num_jugadores == 2:
    print("Jugador 2")
    secuencia_jugador2 = obtener_secuencia(opcion_ingreso)
    rutas_jugador2, todas_rutas_jugador2 = buscar_rutas(secuencia_jugador2, 4, 13)

while not rutas_jugador2:
    if opcion_ingreso==1:
        print(f"No hay rutas ganadoras para el jugador 1 con la combinación: {secuencia_jugador1}. Dame otra:\n")
        secuencia_jugador2 = obtener_secuencia(opcion_ingreso)  # Corregido aquí
        rutas_jugador2, todas_rutas_jugador1 = buscar_rutas(secuencia_jugador1, 4, 13)
    else:
        print(f"No hay rutas ganadoras para el jugador 1 con la combinación: {secuencia_jugador2}"+ "\nCalculando nueva ruta aleatorea")
        longitu_secuencia = random.randint(4, 7)
        secuencia_jugador2 = ''.join(random.choice(['r', 'b']) for _ in range(longitu_secuencia))
        rutas_jugador2, todas_rutas_jugador2 = buscar_rutas(secuencia_jugador2, 4, 13)


with open("Ajedrez/rutas_jugador1_coordenadas.txt", "w") as archivo:
    for ruta in rutas_jugador1:
        # Convertir los números a coordenadas
        ruta_coordenadas = [numero_a_coordenada(numero) for numero in ruta]
        # Escribir la ruta como string de coordenadas
        archivo.write(str(ruta_coordenadas) + "\n")

    with open("Ajedrez/rutas_jugador2_coordenadas.txt", "w") as archivo:
        for ruta in rutas_jugador2:
            # Convertir los números a coordenadas
            ruta_coordenadas = [numero_a_coordenada(numero) for numero in ruta]
            archivo.write(str(ruta_coordenadas) + "\n")

    with open("Ajedrez/rutas_jugador2.txt", "w") as archivo:
        for ruta in rutas_jugador2:
            archivo.write(' '.join(map(str, ruta)) + "\n")

    with open("Ajedrez/todas_rutas_jugador2.txt", "w") as archivo:
        for ruta in todas_rutas_jugador2:
            archivo.write(' '.join(map(str, ruta)) + "\n")
    print(f"Jugador 2: Verifica 'rutas_jugador2.txt' para rutas válidas y 'todas_rutas_jugador2.txt' para todas las rutas exploradas que cumplen con el tamaño de la secuencia.\n")


# Inicialización de Pygame
pygame.init()

# Configuraciones del tablero
TAMANO_CASILLA = 60  # Tamaño de cada casilla en píxeles
TAMANO_TABLERO = 4
ANCHO = ALTO = TAMANO_CASILLA * TAMANO_TABLERO
COLOR1 = (0, 0, 0)  # Color claro para el tablero
COLOR2 = (255, 0, 0)   # Color oscuro para el tablero
COLOR_JUGADOR1 = (0, 255, 0)  # Rojo para el jugador 1
COLOR_JUGADOR2 = (0, 0, 255)  # Azul para el jugador 2
COLOR_TEXTO = (255,255, 255)     

# Configuración de la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego 4x4")
fuente = pygame.font.Font(None, 36)  # None usa la fuente predeterminada de Pygame

def dibujar_tablero():
    for fila in range(TAMANO_TABLERO):
        for columna in range(TAMANO_TABLERO):
            color = COLOR1 if (fila + columna) % 2 == 0 else COLOR2
            pygame.draw.rect(pantalla, color, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))

def cargar_rutas(nombre_archivo):
    """Carga todas las rutas posibles desde el archivo."""
    with open(nombre_archivo, 'r') as archivo:
        rutas = [ast.literal_eval(linea.strip()) for linea in archivo]
    return rutas

def encontrar_ruta_alternativa(rutas_disponibles, ruta_actual, indice_actual):
    """Encuentra una ruta alternativa que siga las mismas posiciones hasta indice_actual."""
    for ruta in rutas_disponibles:
        if ruta[:indice_actual] == ruta_actual[:indice_actual] and len(ruta) > indice_actual:
            # Verifica si la ruta se desvía después del punto de conflicto
            if ruta[indice_actual] != ruta_actual[indice_actual]:
                return ruta
    return None  # No se encontró una ruta alternativa



def dibujar_jugador(posicion, color):
    centro_x = posicion[1] * TAMANO_CASILLA + TAMANO_CASILLA // 2
    centro_y = posicion[0] * TAMANO_CASILLA + TAMANO_CASILLA // 2
    pygame.draw.circle(pantalla, color, (centro_x, centro_y), TAMANO_CASILLA // 4)

    
def mostrar_mensaje(mensaje):
    texto = fuente.render(mensaje, True, COLOR_TEXTO)
    pantalla.blit(texto, (ANCHO / 2 - texto.get_width() / 2, ALTO / 2 - texto.get_height() / 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Espera 3 segundos antes de cerrar el juego

def mostrar_ganador(ganador):
    if ganador == "Empate":
        texto = fuente.render("Empate", True, COLOR_TEXTO)
    else:
        texto = fuente.render(f"Jugador {ganador} gana!", True, COLOR_TEXTO)
    pantalla.blit(texto, (ANCHO / 2 - texto.get_width() / 2, ALTO / 2 - texto.get_height() / 2))
    pygame.display.flip()
    pygame.time.wait(5000)  # Espera 3 segundos antes de cerrar el juego
    pygame.quit()  # Cierra el juego después de mostrar el mensaje

rutas_disponibles_jugador1 = cargar_rutas("Ajedrez/rutas_jugador1_coordenadas.txt")
rutas_disponibles_jugador2 = cargar_rutas("Ajedrez/rutas_jugador2_coordenadas.txt")


if not rutas_disponibles_jugador1 or not rutas_disponibles_jugador2:  # Si la lista está vacía
    print("No hay rutas ganadoras para algún jugador")
    print("Para la secuencia del jugador 1: " + secuencia_jugador1 )
    print("O para la secuencia del jugador 2: " + secuencia_jugador2 )

else:
    def juego():
        pygame.time.wait(3000)
        ruta_jugador1 =random.choice(rutas_disponibles_jugador1)
        ruta_jugador2 =random.choice(rutas_disponibles_jugador2)

        print("Para la secuencia del jugador 1: " + secuencia_jugador1 + "\nSe escogió la ruta:")
        print(ruta_jugador1)
        print("\nPara la secuencia del jugador 2: " + secuencia_jugador2 + "\nSe escogió la ruta:")
        print(ruta_jugador2)
        
        indice_ruta1 = indice_ruta2 = 0
        turno_jugador =random.randint(1, 2)
        print(f"Inicia el jugador: {turno_jugador}")
        contador_turnos = 0
        empate1 = False
        empate2 = False  # Variable para controlar si hay un empate

        reloj = pygame.time.Clock()

        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            dibujar_tablero()
                
                # Chequeo de conflicto antes de mover
            if turno_jugador == 1 and indice_ruta1 +1<len(ruta_jugador1) -1:
                proxima_pos = ruta_jugador1[indice_ruta1 + 1] #if indice_ruta1 + 1 < len(ruta_jugador1) else None
                pos_actual_jugador2 = ruta_jugador2[indice_ruta2] if indice_ruta2 < len(ruta_jugador2) else None

                if proxima_pos == pos_actual_jugador2:
                    print(f"\nConflicto detectado para el Jugador 1 en la posición {proxima_pos}. Buscando ruta alternativa...")
                    ruta_original = ruta_jugador1  # Guarda la ruta original antes de buscar una nueva
                    nueva_ruta = encontrar_ruta_alternativa(rutas_disponibles_jugador1, ruta_jugador1, indice_ruta1 + 1)

                    if nueva_ruta:
                            ruta_jugador1 = nueva_ruta
                            print("Ruta original del Jugador 1:", ruta_original)
                            print("Nueva ruta del Jugador 1:", ruta_jugador1)
                    else:
                            print("No se encontró una ruta alternativa para el Jugador 1. Pierde un turno")
                            turno_jugador=2
                            empate1 = True

                    if not nueva_ruta:
                                proxima_pos_jugador2 = ruta_jugador2[indice_ruta2 + 1]
                                pos_actual_jugador1 = ruta_jugador1[indice_ruta1] if indice_ruta1 < len(ruta_jugador1) else None

                                if proxima_pos_jugador2 == pos_actual_jugador1:
                                    print(f"Conflicto detectado para el Jugador 1 en la posición {proxima_pos_jugador2}. Buscando ruta alternativa...")
                                    ruta_original = ruta_jugador2
                                    nueva_ruta = encontrar_ruta_alternativa(rutas_disponibles_jugador2, ruta_jugador2, indice_ruta2 + 1)

                                    if nueva_ruta:
                                        ruta_jugador2 = nueva_ruta
                                        print("Ruta original del Jugador 2:", ruta_original)
                                        print("Nueva ruta del Jugador 2:", ruta_jugador2)
                                    else:
                                        print("No se encontró una ruta alternativa para el Jugador 1. Pierde un turno")
                                        turno_jugador = 1
                                        empate2 = True    

                            

            elif    turno_jugador==2 and indice_ruta2 + 1 < len(ruta_jugador2) -1:
                    proxima_pos = ruta_jugador2[indice_ruta2 + 1]
                    pos_actual_jugador1 = ruta_jugador1[indice_ruta1] if indice_ruta1 < len(ruta_jugador1) else None

                    if proxima_pos == pos_actual_jugador1:
                        print(f"Conflicto detectado para el Jugador 2 en la posición {proxima_pos}. Buscando ruta alternativa...")
                        ruta_original = ruta_jugador2  # Guarda la ruta original antes de buscar una nueva
                        nueva_ruta = encontrar_ruta_alternativa(rutas_disponibles_jugador2, ruta_jugador2, indice_ruta2 + 1)

                        if nueva_ruta:
                            ruta_jugador2 = nueva_ruta
                            print("Ruta original del Jugador 2:", ruta_original)
                            print("Nueva ruta del Jugador 2:", ruta_jugador2)
                        else:
                            print("No se encontró una ruta alternativa para el Jugador 2. Pierde un turno")
                            turno_jugador=1
                            empate2 =True

                            # Después de que el jugador 2 pierda un turno, verifica si el jugador 1 también pierde un turno por falta de rutas alternativas
                        if not nueva_ruta:
                            proxima_pos_jugador1 = ruta_jugador1[indice_ruta1 + 1]
                            pos_actual_jugador2 = ruta_jugador2[indice_ruta2] if indice_ruta2 < len(ruta_jugador2) else None

                            if proxima_pos_jugador1 == pos_actual_jugador2:
                                print(f"Conflicto detectado para el Jugador 1 en la posición {proxima_pos_jugador1}. Buscando ruta alternativa...")
                                ruta_original = ruta_jugador1
                                nueva_ruta = encontrar_ruta_alternativa(rutas_disponibles_jugador1, ruta_jugador1, indice_ruta1 + 1)

                                if nueva_ruta:
                                    ruta_jugador1 = nueva_ruta
                                    print("Ruta original del Jugador 1:", ruta_original)
                                    print("Nueva ruta del Jugador 1:", ruta_jugador1)
                                else:
                                    print("No se encontró una ruta alternativa para el Jugador 1. Pierde un turno")
                                    turno_jugador = 2
                                    empate1 = True                        


            if  empate1 and empate2:
                print("No hay más rutas disponibles para ningun jugador, es un empate")
                mostrar_ganador("Empate")
                corriendo = False
                break


            if indice_ruta1 < len(ruta_jugador1):
                dibujar_jugador(ruta_jugador1[indice_ruta1], COLOR_JUGADOR1)
            else:
                mostrar_ganador(1)
                break

            if indice_ruta2 < len(ruta_jugador2):
                dibujar_jugador(ruta_jugador2[indice_ruta2], COLOR_JUGADOR2)
            else:
                mostrar_ganador(2)
                break

            pygame.display.flip()

            if turno_jugador == 1 and indice_ruta1 < len(ruta_jugador1):
                indice_ruta1 += 1
                turno_jugador = 2
            elif turno_jugador == 2 and indice_ruta2 < len(ruta_jugador2):
                indice_ruta2 += 1
                turno_jugador = 1

            contador_turnos += 1  
            reloj.tick(1)


        pygame.quit()

    juego()

import matplotlib.pyplot as plt
import networkx as nx

def dibujar_grafo_desde_archivo(archivo, mensaje):


    
    G = nx.DiGraph()

    
    with open(archivo, 'r') as f:
        rutas = [line.strip().split() for line in f]
        longitud_ruta = len(rutas[0])

        
        posiciones = {}
        for idx, ruta in enumerate(rutas):
            for pos, estado in enumerate(ruta):
                nodo = (pos + 1, int(estado))
                if nodo not in posiciones:
                    posiciones[nodo] = (pos, -idx)
                if pos < longitud_ruta - 1:
                    nodo_siguiente = (pos + 2, int(ruta[pos + 1]))
                    G.add_edge(nodo, nodo_siguiente)

    
    plt.figure(figsize=(9, 8))
    
    
    num_columnas = longitud_ruta
    
    
    distancia_entre_columnas = 2  
    
    
    for columna in range(1, num_columnas + 1):
        nodos_en_columna = [nodo for nodo in posiciones.keys() if nodo[0] == columna]
        
        for idx, nodo in enumerate(nodos_en_columna):
            posiciones[nodo] = (columna, -idx * distancia_entre_columnas)
    
    
    nx.draw(G, pos=posiciones, with_labels=False, node_size=800, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
    
    
    etiquetas = {nodo: f"{nodo[1]}" for nodo in G.nodes()}
    nx.draw_networkx_labels(G, pos=posiciones, labels=etiquetas, font_color='black', font_size=8)
    
   
    plt.text(0.5, 0.95, mensaje, ha='center', va='center', fontsize=12, transform=plt.gca().transAxes)
    
    plt.title('Graph of Node Connections Across Positions')
    plt.axis('off')
    plt.show()


# ruta_a_tu_archivo.txt = 'ruta_a_tu_archivo.txt'  
dibujar_grafo_desde_archivo('Ajedrez/todas_rutas_jugador1.txt', "Red del jugador 1")
dibujar_grafo_desde_archivo('Ajedrez/todas_rutas_jugador2.txt', "Red del jugador 2")