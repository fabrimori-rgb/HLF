import numpy as np
import variables as v

def crear_tablero(tamano=v.TAMANO_TABLERO):
    tablero = np.full((tamano, tamano), v.AGUA, dtype=str)
    return tablero

#funcion para crear el tablero con numero de filas y columnas
def imprimir_tablero(tablero):
    tamano = len(tablero)

    #cabecera de columnas (1 a 10 con espacio para separa el 9 del 10)
    cabecera_columnas = "   " + " ".join(f"{i:<2}" for i in range(1, tamano + 1))
    print(cabecera_columnas)
    print("-----" + "---" * tamano)

    #filas con su respectivo numero al lado
    for i in range(tamano):
        numero_fila = f"{i + 1:2d}"
        elementos_fila = "".join(f"{celda} " for celda in tablero[i])
        print(f"{numero_fila}|{elementos_fila}")

# ejecutar la funcion
if __name__ == "__main__":
    tablero_jugador = crear_tablero()
    tablero_disparos_jugador = crear_tablero()
    tablero_rival = crear_tablero()
    tablero_disparos_rival = crear_tablero()

# COLOCAR LA FLOTA EN EL TABLERO
# colocar los barcos en el tablero - con atributo .shape, que devuelve el atributo de np para extraer las dimensiones de la matriz, separándolas en las variables filas y columnas
# el sistema de intentos busca colocar la flota completa un max de 100 veces (bucle de seguridad)
# en cada intento crea una copia limpia del tablero vaciandola con la variable.AGUA
# calculo de las posiciones validas de los barcos: la funcion calcula donde puede empezar un barco sin salirse de los bordes del tablero 
# Horizontal ("H"): La columna inicial (c) no puede superar el límite menos la longitud del barco (columnas - longitud + 1). Lo mismo para Vertical (V)
# creacion de las casillas y control solapamiento: para cada posicion valida, crea la lista completa de casillas ocupadas por el barco
# funcion .all comprueba si todas las casillas estan libres (AGUA), en este caso la opcion se anade a las opciones validas .append
# en caso contrario break y vuelta a empezar. si hay opciones disposicion random de los barcos random.choice(opciones)
# si fallo en 100 intentos, error RuntimeError


import random

def colocar_barcos(tablero):
    esloras = v.ESLORA_BARCO
    filas, columnas = tablero.shape

    for intento in range(100):
        tablero_prueba = tablero.copy()
        tablero_prueba[:] = v.AGUA
        colocacion_completa = True

        for longitud in esloras:
            opciones = []

            for direccion in ("H", "V"):
                if direccion == "H":
                    inicios = [(f, c)
                        for f in range(filas)
                        for c in range(columnas - longitud + 1)]
                else:
                    inicios = [(f, c)
                        for f in range(filas - longitud + 1)
                        for c in range(columnas)]

                for fila, columna in inicios:
                    casillas = [(fila, columna + paso) if direccion == "H"
                        else (fila + paso, columna)
                        for paso in range(longitud)]

                    if all(tablero_prueba[f, c] == v.AGUA
                           for f, c in casillas):
                        opciones.append(casillas)

            if not opciones:
                colocacion_completa = False
                break

            for fila, columna in random.choice(opciones):
                tablero_prueba[fila, columna] = v.BARCO

        if colocacion_completa:
            return tablero_prueba

    raise RuntimeError("No se pudo colocar toda la flota; inténtalo de nuevo.")

def imprimir_cuatro_tableros(tablero_jugador_flota, tablero_jugador_disparos, tablero_rival_flota, tablero_rival_disparos):
    """
    Imprime de forma clara las 4 pantallas solicitadas:
    - Dos del jugador (Mi flota, Mis disparos)
    - Dos del rival (Flota rival, Disparos rival)
    """
    print("\n" + "="*50)
    print("                 ESTADO DEL JUEGO                 ")
    print("="*50)
    
    print("\n🌊 [1] TU FLOTA (Tus barcos y ataques recibidos):")
    print(tablero_jugador_flota)
    
    print("\n🎯 [2] TUS DISPAROS (Tus ataques al enemigo):")
    print(tablero_jugador_disparos)
    
    print("\n🚢 [3] FLOTA RIVAL (Tablero oculto del rival):")
    print(tablero_rival_flota)
    
    print("\n💥 [4] DISPAROS RIVAL (Ataques ejecutados por la máquina):")
    print(tablero_rival_disparos)
    print("="*50)

def turno_disparo_jugador(tablero_rival_flota, tablero_jugador_disparos):
    """
    Gestiona mi disparos sobre el tablero rival.
    Actualiza el tablero de mis disparos y el tablero real del rival.
    """
    filas, columnas = tablero_rival_flota.shape
    while True:
        try:
            print("\n--- TU TURNO DE DISPARO ---")
            f = int(input(f"Introduce la fila (0 a {filas-1}): "))
            c = int(input(f"Introduce la columna (0 a {columnas-1}): "))
            
            if not (0 <= f < filas and 0 <= c < columnas):
                print("⚠️ Coordenadas fuera de rango. Inténtalo de nuevo.")
                continue
                
            if tablero_jugador_disparos[f, c] != v.AGUA:
                print("⚠️ Ya has disparado en esta casilla. Elige otra.")
                print(tablero_jugador_disparos)
                continue
                
            # Evaluar impacto en la flota rival
            if tablero_rival_flota[f, c] == v.BARCO:
                tablero_rival_flota[f, c] = v.TOCADO
                tablero_jugador_disparos[f, c] = v.TOCADO
                print("\n🎯 ¡IMPACTO! ¡Has tocado un barco enemigo!")
                print(tablero_jugador_disparos)
                return "tocado"
            else:
                tablero_rival_flota[f, c] = v.AGUA_DISPARO
                tablero_jugador_disparos[f, c] = v.AGUA_DISPARO
                print("\n🌊 ¡Agua! Has fallado el disparo.")
                print(tablero_jugador_disparos)
                return "agua"
                
        except ValueError:
            print("⚠️ Entrada inválida. Introduce un número entero.")

def turno_disparo_rival(tablero_jugador_flota, tablero_rival_disparos):
    """
    Gestiona el disparo automático de la máquina contra el jugador.
    Evita repetir coordenadas ya disparadas previamente.
    """
    filas, columnas = tablero_jugador_flota.shape
    
    while True:
        f = random.randint(0, filas - 1)
        c = random.randint(0, columnas - 1)
        
        # Comprobar que la máquina no repita disparo en la misma casilla
        if tablero_rival_disparos[f, c] == v.AGUA:
            break
            
    print(f"\n🤖 El rival (máquina) dispara a la coordenada: Fila {f}, Columna {c}")
    
    if tablero_jugador_flota[f, c] == v.BARCO:
        tablero_jugador_flota[f, c] = v.TOCADO
        tablero_rival_disparos[f, c] = v.TOCADO
        print("💥 ¡La máquina ha tocado uno de tus barcos!")
        print(tablero_rival_disparos)
        return "tocado"
        
    else:
        tablero_jugador_flota[f, c] = v.AGUA_DISPARO
        tablero_rival_disparos[f, c] = v.AGUA_DISPARO
        print("💨 La máquina ha disparado al agua.")
        print(tablero_rival_disparos)
        return "agua"
        
