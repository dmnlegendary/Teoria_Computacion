import pygame
import random
import ast


pygame.init()

# Configuraciones del tablero
TAMANO_CASILLA = 60  # Tamaño de cada casilla en píxeles
TAMANO_TABLERO = 4
ANCHO = ALTO = TAMANO_CASILLA * TAMANO_TABLERO
COLOR1 = (0, 0, 0)  # Color claro para el tablero
COLOR2 = (255, 0, 0)   # Color oscuro para el tablero
COLOR_JUGADOR1 = (0, 255, 0)  # Rojo para el jugador 1
COLOR_JUGADOR2 = (0, 0, 255)  # Azul para el jugador 2
COLOR_TEXTO = (0,255, 0)       # Negro para el texto

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
    # print("Para la secuencia del jugador 1: " + secuencia_jugador1 )
    # print("O para la secuencia del jugador 2: " + secuencia_jugador2 )

else:
    def juego():
        pygame.time.wait(3000)
        ruta_jugador1 = random.choice(rutas_disponibles_jugador1)
        ruta_jugador2 = random.choice(rutas_disponibles_jugador2)

        # print("Para la secuencia del jugador 1: " + secuencia_jugador1 + "\nSe escogió la ruta:")
        print(ruta_jugador1)
        # print("\nPara la secuencia del jugador 2: " + secuencia_jugador2 + "\nSe escogió la ruta:")
        print(ruta_jugador2)
        
        indice_ruta1 = indice_ruta2 = 0
        turno_jugador =random.randint(1, 2)
        print(f"Inicia el jugador: {turno_jugador}")
        contador_turnos = 0
        contador_rondas=0
        empate1 = False
        empate2 = False  # Variable para controlar si hay un empate
        dejarpasar=False

        reloj = pygame.time.Clock()

        corriendo = True
        juego_activo=True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                    juego_activo=False


            if juego_activo:
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
                    juego_activo=False 
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

                contador_turnos += 1  # Incrementa el contador de turnos
                reloj.tick(1)


        pygame.quit()

    juego()

