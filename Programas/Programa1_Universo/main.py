# Diaz Jimenez Jorge Arif 5BM2

import itertools
import math
import matplotlib.pyplot as plt

def generar_cadenas_binarias(n):
    return [''.join(seq) for seq in itertools.product('01', repeat=n)]

def contar_unos_y_ceros(cadenas):
    conteo_unos = [cadena.count('1') for cadena in cadenas]
    conteo_ceros = [len(cadena) - unos for cadena, unos in zip(cadenas, conteo_unos)]
    return conteo_unos, conteo_ceros

def guardar_en_archivo(cadenas, filename):
    with open(filename, 'w') as file:
        file.write("{\n")
        file.write(",\n".join(cadenas))
        file.write("\n}")

def graficar_datos(cadenas, unos, ceros, filename):
    x = range(len(cadenas))
    
    plt.bar(x, unos, color='b', label='Unos')
    plt.bar(x, ceros, bottom=unos, color='r', label='Ceros')
    plt.xlabel('Cadenas Binarias')
    plt.ylabel('Cantidad')
    plt.title('Número de Unos y Ceros por Cadena Binaria')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def graficar_logaritmo(cadenas, unos, ceros, filename):
    x = range(len(cadenas))
    log_unos = [math.log10(u+1) for u in unos]  # Evitar log(0)
    log_ceros = [math.log10(c+1) for c in ceros]  # Evitar log(0)

    plt.bar(x, log_unos, color='b', label='Log(Unos)')
    plt.bar(x, log_ceros, bottom=log_unos, color='r', label='Log(Ceros)')
    plt.xlabel('Cadenas Binarias')
    plt.ylabel('Logaritmo Base 10')
    plt.title('Logaritmo del Número de Unos y Ceros por Cadena Binaria')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def main():
    while True:
        modo = input("¿Modo automático (A) o manual (M)? ").strip().upper()
        
        if modo == 'A':
            for n in range(1001):
                cadenas = generar_cadenas_binarias(n)
                filename = f'cadenas_binarias_n{n}.txt'
                guardar_en_archivo(cadenas, filename)
                
                unos, ceros = contar_unos_y_ceros(cadenas)
                graficar_datos(cadenas, unos, ceros, f'grafico_unos_ceros_n{n}.png')
                graficar_logaritmo(cadenas, unos, ceros, f'grafico_log_unos_ceros_n{n}.png')

        elif modo == 'M':
            n = int(input("Introduce el valor de n (0-1000): "))
            cadenas = generar_cadenas_binarias(n)
            filename = f'cadenas_binarias_n{n}.txt'
            guardar_en_archivo(cadenas, filename)
            
            unos, ceros = contar_unos_y_ceros(cadenas)
            graficar_datos(cadenas, unos, ceros, f'grafico_unos_ceros_n{n}.png')
            graficar_logaritmo(cadenas, unos, ceros, f'grafico_log_unos_ceros_n{n}.png')

        else:
            print("Opción no válida.")

        continuar = input("¿Calcular otra 'n'? (S/N) ").strip().upper()
        if continuar != 'S':
            break

if __name__ == '__main__':
    main()
