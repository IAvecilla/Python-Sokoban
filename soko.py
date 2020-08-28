import copy

PARED = "#"
CAJA = "$"
JUGADOR = "@"
OBJETIVO = "."
OBJETIVO_CAJA = "*"
OBJETIVO_JUGADOR = "+"
ESPACIO_VACIO = " "

OESTE = (-1, 0)
ESTE = (1, 0)
NORTE = (0, -1)
SUR = (0, 1)

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
    
    grilla = []
    
    for f in range (len(desc)):
        fila = []
        for c in range(len(desc[f])):
            fila.append(desc[f][c])
        
        grilla.append(fila)
    
    return grilla

def dimensiones (grilla):
    '''
    Devuelve una tupla con la cantidad de columnas y filas de la grilla.
    '''
    cantidad_filas = len(grilla)
    cantidad_columnas = len(grilla[0])
    
    return (cantidad_columnas, cantidad_filas)

def hay_pared (grilla, c, f):
    '''
    Devuelve True si hay una pared en la columna y fila (c, f).
    '''
    return grilla [f][c] == PARED

def hay_objetivo (grilla, c, f):
    '''
    Devuelve True si hay un objetivo en la columna y fila (c, f).
    '''
    return grilla [f][c] == OBJETIVO or grilla [f][c] == OBJETIVO_JUGADOR or grilla [f][c] == OBJETIVO_CAJA

def hay_caja (grilla, c, f):
    '''
    Devuelve True si hay una caja en la columna y fila (c, f).
    '''
    return grilla [f][c] == CAJA or grilla [f][c] == OBJETIVO_CAJA

def hay_jugador (grilla, c, f):
    '''
    Devuelve True si el jugador está en la columna y fila (c, f).
    '''
    return grilla [f][c] == JUGADOR or grilla[f][c] == OBJETIVO_JUGADOR

def hay_espacio (grilla, c, f):
    '''
    Devuelve True si hay un espacio vacio en la columna y fila (c, f)
    '''
    return grilla [f][c] == ESPACIO_VACIO
    
def juego_ganado (grilla):
    '''
    Devuelve True si el juego esta ganado
    '''
    for filas in grilla:
        if CAJA in filas:
            return False
    return True
    
      
def mover(grilla, direccion):
    '''
    Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    ''' 
    for f in range (len(grilla)):
        for c in range(len(grilla[f])):
            if grilla[f][c] == JUGADOR or grilla [f][c] == OBJETIVO_JUGADOR:
                fila = f
                col = c
                break
    
    # Realizo la copia de la grilla original
    nueva_grilla = copy.deepcopy (grilla)
    
    # Guardo la posicion que esta un casillero mas adelante 
    pos_sig = grilla [fila + (direccion[1])] [col + (direccion [0])]
            
    if pos_sig == PARED:
        return grilla
    
    # Guardo la posicion que está dos casilleros mas adelante
    pos_sig_sig = grilla [fila + 2 * (direccion[1])] [col + 2 * (direccion[0])]
   
    if (pos_sig == CAJA or pos_sig == OBJETIVO_CAJA) and (pos_sig_sig == CAJA or pos_sig_sig == PARED or pos_sig_sig == OBJETIVO_CAJA):
        return grilla
    
    mover_caja (grilla, direccion, pos_sig, fila, col, nueva_grilla, pos_sig_sig)
    mover_jugador (grilla, direccion, pos_sig, fila, col, nueva_grilla, pos_sig_sig)
    return nueva_grilla
    
def mover_jugador (grilla, direccion, pos_sig, fila, col, nueva_grilla, pos_sig_sig):
    """
    En caso de que este permitido mueve al jugador a la posicion deseada
    """
    if pos_sig == ESPACIO_VACIO and grilla[fila][col] == JUGADOR:
        nueva_grilla [fila][col] = ESPACIO_VACIO
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = JUGADOR
        
    elif pos_sig == ESPACIO_VACIO and grilla[fila][col] == OBJETIVO_JUGADOR:
        nueva_grilla [fila][col] = OBJETIVO
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = JUGADOR
    
    elif pos_sig == CAJA and grilla[fila][col] == OBJETIVO_JUGADOR and pos_sig_sig == ESPACIO_VACIO:
        nueva_grilla [fila][col] = OBJETIVO
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = JUGADOR
        nueva_grilla [fila + 2 * (direccion[1])] [col + 2 * (direccion[0])] = CAJA
        
    elif pos_sig == OBJETIVO and grilla[fila][col] == JUGADOR:
        nueva_grilla [fila][col] = ESPACIO_VACIO
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = OBJETIVO_JUGADOR
    
    elif pos_sig == OBJETIVO_CAJA and grilla[fila][col] == OBJETIVO_JUGADOR:
        nueva_grilla [fila][col] = OBJETIVO
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = OBJETIVO_JUGADOR
    
    elif pos_sig == OBJETIVO and grilla[fila][col] == OBJETIVO_JUGADOR:
        nueva_grilla [fila][col] = OBJETIVO
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = OBJETIVO_JUGADOR
    
    elif pos_sig == OBJETIVO_CAJA and grilla[fila][col] == JUGADOR:
        nueva_grilla [fila][col] = ESPACIO_VACIO
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = OBJETIVO_JUGADOR
    
    elif pos_sig == CAJA and grilla[fila][col] == JUGADOR:
        nueva_grilla [fila][col] = ESPACIO_VACIO
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = JUGADOR
    
    elif pos_sig == CAJA and grilla[fila][col] == OBJETIVO_JUGADOR:
        nueva_grilla [fila][col] = OBJETIVO
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = JUGADOR

def mover_caja (grilla, direccion, pos_sig, fila, col, nueva_grilla, pos_sig_sig):
    """
    En caso de que este permitido mueve a la caja a la posicion deseada
    """
    if pos_sig == CAJA and pos_sig_sig == ESPACIO_VACIO:
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = ESPACIO_VACIO
        nueva_grilla [fila + 2 * (direccion[1])] [col + 2 * (direccion[0])] = CAJA
        
    elif pos_sig == CAJA and pos_sig_sig == OBJETIVO:
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = ESPACIO_VACIO
        nueva_grilla [fila + 2 * (direccion[1])] [col + 2 * (direccion[0])] = OBJETIVO_CAJA
        
    elif pos_sig == OBJETIVO_CAJA and pos_sig_sig == ESPACIO_VACIO:
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = OBJETIVO
        nueva_grilla [fila + 2 * (direccion[1])] [col + 2 * (direccion[0])] = CAJA
    
    elif pos_sig_sig == ESPACIO_VACIO and pos_sig == OBJETIVO_CAJA:
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = OBJETIVO
        nueva_grilla [fila + 2 * (direccion[1])] [col + 2 * (direccion[0])] = CAJA
    
    elif pos_sig_sig == OBJETIVO and pos_sig == OBJETIVO_CAJA:
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = OBJETIVO
        nueva_grilla [fila + 2 * (direccion[1])] [col + 2 * (direccion[0])] = OBJETIVO_CAJA
    
    elif pos_sig_sig == OBJETIVO and pos_sig == CAJA:
        nueva_grilla [fila + direccion[1]] [col + direccion[0]] = ESPACIO_VACIO
        nueva_grilla [fila + 2 * (direccion[1])] [col + 2 * (direccion[0])] = OBJETIVO_CAJA
    
        

    
      
