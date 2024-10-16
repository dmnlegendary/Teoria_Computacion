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

# def convertir_rutas_a_coordenadas(ruta):
#     return [numero_a_coordenada(numero) for numero in ruta]

def es_valida(x, y):
    return 0 <= x < TAMANO_TABLERO and 0 <= y < TAMANO_TABLERO

def coordenada_a_numero(x, y):
    return x * TAMANO_TABLERO + y + 1

def explorar_ruta(x, y, secuencia, ruta_actual, rutas, casilla_final, todas_rutas, longitud_secuencia):
    # print("Ruta actual (en números de casillas):", ruta_actual)  

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
        longitu_secuencia = random.randint(4, 10)
        return ''.join(random.choice(['r', 'b']) for _ in range(longitu_secuencia))
    

opcion_ingreso = int(input("Elige el modo de ingreso de secuencias (1 para manual, 2 para aleatorio): "))
num_jugadores = 2


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
        longitu_secuencia = random.randint(4, 10)
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
        longitu_secuencia = random.randint(4, 10)
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

