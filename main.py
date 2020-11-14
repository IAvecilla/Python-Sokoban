import soko
import gamelib
from pila import Pila
from cola import Cola

def transformar_formato (nivel):
    """
    Recibe el nivel en forma de lista y lo devuelve en formato de tuplas no mutables
    """
    nivel_tupla = ()
    for lista in nivel:
        nivel_tupla += tuple(lista)
    
    return nivel_tupla

def buscar_solucion (estado_inicial):
    visitados = {}
    return backtrack (estado_inicial, visitados)

def backtrack (estado, visitados):
    """
    Ejecuta de manera recursiva un algoritmo de Backtracking para encontrar los movimiento a seguir para resolver el nivel
    Recibe el estado del juego y los estados ya visitados.
    En caso de exito devuelve true y una lista que contiene los movimientos indicados
    """
    visitados [transformar_formato(estado)] = "estado"
    if soko.juego_ganado(estado):
        return True, Pila()
    for a in (movimientos_posibles(estado)):
        nuevo_estado = soko.mover(estado, a)
        if transformar_formato(nuevo_estado) in visitados:
            continue
        solucion_encontrada, acciones = backtrack(nuevo_estado, visitados)
        if solucion_encontrada:
            acciones.apilar(a)
            return True, acciones
    
    return False, None

def movimientos_posibles (estado):
    """
    Recibe el estado actual del juego y devuele una lista con los movimientos posibles a realizar
    """
    movimientos = [(1, 0),(0, 1),(-1, 0),(0, -1)]
    posibles = []
    for m in movimientos:
        if soko.mover(estado, m) != estado:
            posibles.append(m)
    
    return posibles

def dibujar_nivel (nivel):
    """"
    Recibe el nivel actual y se encarga de dibujarlo por pantalla
    """

    for f in range (len(nivel)):
            for c in range(len(nivel[f])):
                gamelib.draw_image('img/ground.gif', c * 64, f * 64)
                
                if soko.hay_jugador(nivel, c, f):
                    pos_jugador_y = c * 64  
                    pos_jugador_x = f * 64
                    gamelib.draw_image('img/player.gif', pos_jugador_y, pos_jugador_x)
                
                if soko.hay_pared(nivel, c, f):
                    pos_pared_y = c * 64 
                    pos_pared_x = f * 64
                    gamelib.draw_image('img/wall.gif', pos_pared_y, pos_pared_x)
                
                if soko.hay_caja(nivel, c, f):
                    pos_caja_y = c * 64  
                    pos_caja_x = f * 64
                    gamelib.draw_image('img/box.gif', pos_caja_y, pos_caja_x)
                
                if soko.hay_objetivo(nivel, c, f):
                    pos_objetivo_y = c * 64  
                    pos_objetivo_x = f * 64
                    gamelib.draw_image('img/goal.gif', pos_objetivo_y, pos_objetivo_x)
                

def cargar_niveles (ruta_archivo):
    """
    Recibe la ruta de un archivo y devuelve una lista de listas, donde cada sublista es un nivel
    """
    max_longitud_fila = 0
    
    with open (ruta_archivo) as archivo:
        total_niveles = archivo.readlines()
        nivel = []
        niveles = []
        
        for fila in total_niveles:
            fila = fila[:-1]
            
            if not "#" in fila and fila != "":
                continue
            
            if fila == "":
                for i in range (len(nivel)):
                    nivel[i] += (" " * (max_longitud_fila - len(nivel[i])))
                
                niveles.append(nivel)
                nivel = []
                max_longitud_fila = 0
                continue
            
            if len(fila) > max_longitud_fila:
                max_longitud_fila = len(fila)
                
            nivel.append(fila)
        
        return niveles
    
def cargar_teclas (ruta_archivo):
    """
    Recibe un archivo con las teclas del juego y devuelve un diccionario cuyas claves son las teclas y los valores el movimiento asignado
    """
    with open ("teclas.txt") as controles:
            teclas_por_accion = {}
            
            for linea in controles:
                teclas = linea.rstrip("\n").split(" = ")
        
                if teclas == [""]:
                    continue
        
                letra = teclas [0]
                accion = teclas [1]
        
                if accion == "NORTE":
                    teclas_por_accion [letra] = (0, -1)
                elif accion == "SUR":
                    teclas_por_accion [letra] = (0, 1)
                elif accion == "ESTE":
                    teclas_por_accion [letra] = (1, 0)
                elif accion == "OESTE":
                    teclas_por_accion [letra] = (-1, 0)
                else:
                    teclas_por_accion [letra] = accion
                    continue
        
    return teclas_por_accion

def redibujar_tablero (nivel, mensaje):
    """
    Recibe el nivel y un mensaje, redibuja el nivel con el mensaje pasado por parametro
    """

    gamelib.draw_begin()

    dibujar_nivel(nivel)
    gamelib.draw_text(mensaje, 50, 15)

    gamelib.draw_end()



def main():
    # Inicializar el estado del juego
    nivel_actual = int(input("Dame el nivel: "))
    pila_aux = Pila()
    cola_aux = Cola()

    controles = cargar_teclas ("teclas.txt")
    niveles = cargar_niveles ("niveles.txt")
    
    nivel = soko.crear_grilla(niveles[nivel_actual])
    
    tamaño_ventana_x, tamaño_ventana_y = soko.dimensiones(nivel)
    gamelib.resize(tamaño_ventana_x * 64, tamaño_ventana_y * 64)
    
    while gamelib.is_alive():
        # Dibujar la pantalla
        gamelib.draw_begin()
        dibujar_nivel(nivel)
        
        #Chequea si se pidieron pistas
        if not cola_aux.esta_vacia():
            gamelib.draw_text("Pista Disponible", 65, 15)
        
        gamelib.draw_end()
        
        # Actualizar el estado del juego, según la `tecla` presionada
        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break
        
        tecla = ev.key
        
        accion = controles.get (tecla)
        
        if accion == "REINICIAR":
            nivel = soko.crear_grilla(niveles[nivel_actual])
            while not pila_aux.esta_vacia():
                pila_aux.desapilar()
            while not cola_aux.esta_vacia():
                cola_aux.desencolar()
            continue
        
        elif accion == "SALIR":
            break
        
        elif accion == "DESHACER":
            while not cola_aux.esta_vacia():
                cola_aux.desencolar()
            if not pila_aux.esta_vacia():
                nivel = pila_aux.desapilar()
                continue
            else:
                continue 
        
        elif accion == "PISTAS":
            if cola_aux.esta_vacia():
                redibujar_tablero(nivel, "Pensando...")
                
                encontrado, pasos = buscar_solucion(nivel)
                if encontrado:
                    while not pasos.esta_vacia():
                        cola_aux.encolar(pasos.desapilar())
                continue
            else:
                direccion = cola_aux.desencolar()
        
        elif tecla in controles:
            while not cola_aux.esta_vacia():
                cola_aux.desencolar()
            direccion = controles[tecla]
        
        else:
            continue
        
        #Update del nivel una vez efectuado el movimiento
        pila_aux.apilar(nivel)
        nivel = soko.mover (nivel, direccion)
        
        
        #Chequea el fin del nivel y pasa al siguiente
        if soko.juego_ganado (nivel):
            nivel_actual += 1
            
            if nivel_actual == len(niveles):
                return
            
            while not pila_aux.esta_vacia():
                pila_aux.desapilar()
            
            nivel = soko.crear_grilla(niveles[nivel_actual])
            
            tamaño_ventana_x, tamaño_ventana_y = soko.dimensiones(nivel)
            gamelib.resize(tamaño_ventana_x * 64, tamaño_ventana_y * 64)
        
            
gamelib.init(main)





