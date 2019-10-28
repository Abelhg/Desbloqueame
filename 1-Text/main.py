# -*- encoding=utf-8 -*-

from subprocess import call

# CARACTERES DEL TABLERO
COE = u'\u2500'  # ─
CNS = u'\u2502'  # │
CES = u'\u250C'  # ┌
CSO = u'\u2510'  # ┐
CNE = u'\u2514'  # └
CON = u'\u2518'  # ┘
COES = u'\u252C' # ┬
CNES = u'\u251C' # ├
CONS = u'\u2524' # ┤
CONE = u'\u2534' # ┴
CSOM = u'\u2593' # ▒

MS = CES + 6*(COES + 4*COE) + CSO  # Marco superior
MI = CNE + 6*(CONE + 4*COE) + CON  # Marco inferior
FILI = [ CNES, CNS, CNS ] # Lado izquierdo de todas las filas
FILD = [ CONS, CNS, CNS ] # Lado derecho de fila normal
FILED = [ CSOM, CSOM, CSOM ] # Lado derecho de fila especial

# Nombres de ficheros
ficNiv = "niveles.txt"
ficPun = "records.txt"

limpiadoPantalla = True

# Objeto Coche
class Coche: 
	# Constructor: nombre, orientación, coordenada_X, coordenada_Y, longitud
    def __init__(self, nom, ori, x, y, lon):
        self.nombre = nom 
        self.orientacion = ori
        self.posX = int(x)
        self.posY = int(y)
        self.longitud = int(lon)     

class Tablero:
	# Constructor: nivel a jugar
    def __init__(self, nivel):
        self.nivel = nivel
        self.modificarTablero() # Lo configura a su estado inicial
        
    # Imprime el tablero con los coches
    def mostrarTablero(self, numniv, movs, record):
        print "NIVEL", numniv, "     Nº DE MOVIMIENTOS:", movs,"     RÉCORD:",
        if(record == 0):
            print "-"
        else:
            print record

        print MS # Imprime el marco superior
        for i in xrange(len(self.tablero)): # Recorre las filas del tablero
            for j in xrange(len(self.tablero[0][0])): # Recorre las subfilas 
                s = FILI[j] # Inicia la string a imprimir con el lado izquierdo
                for k in xrange(len(self.tablero[i])): # Recorre las columnas 
                    if i != 2 or k != 6: # No imprime la ultima parte de la fila 3 (salida)
                        s += self.tablero[i][k][j] # Concatena las columnas de la subfila
                if i != 2: # Dependiendo de si es la tercera fila, imprime un lado derecho especial o no
                    s += FILD[j]
                else:
                    s += FILED[j] + self.tablero[2][6][j]
                print s
        print MI # Imprime el marco inferior
    
    # Vacía el tablero
    def vaciarTablero(self):
        vacio = [ 5*" ", 5*" ", 5*" "]
        tab = []
        for i in xrange(6):
        	if i == 2: tab.append([ vacio, vacio, vacio, vacio, vacio, vacio, vacio ])
        	else: tab.append([ vacio, vacio, vacio, vacio, vacio, vacio ])
        self.tablero = tab

    # Modifica el tablero
    def modificarTablero(self):
        self.vaciarTablero()
        for coche in self.nivel:
            x = coche.posX - 1
            y = coche.posY - 1 
            nom = coche.nombre
            
            for i in xrange(coche.longitud):
                if coche.orientacion == "H":
                    if i == 0:
                        self.tablero[y][x] = [ CES + 4*COE, CNS + nom + 3*" ", CNE + 4*COE ] # Casilla de parte izquierda de coche horizontal
                    elif i == coche.longitud-1:
                        self.tablero[y][x+i] = [ 4*COE + CSO, 3*" " + nom.lower() + CNS, 4*COE + CON ] # Casilla de parte derecha de coche horizontal
                    else:
                        self.tablero[y][x+i] = [ 5*COE, 5*" ", 5*COE ] # Casilla intermedia de coche horizontal
                else:
                    if i == 0:
                        self.tablero[y][x] = [ CES + 3*COE + CSO, CNS + " " + nom + " " + CNS, CNS + 3*" " + CNS ] # Casilla de parte superior de coche vertical
                    elif i == coche.longitud-1:
                        self.tablero[y+i][x] = [ CNS + 3*" " + CNS, CNS + " " + nom.lower() + " " + CNS, CNE + 3*COE + CON ] # Casilla de parte inferior de coche vertical
                    else:
                        self.tablero[y+i][x] = [ CNS + 3*" " + CNS, CNS + 3*" " + CNS,CNS + 3*" " + CNS ] # Casilla de parte intermedia de coche vertical

    # Realiza los movimientos elegidos, comprobando su validez
    def realizarMovimientos(self, movimientos):
        valido = True
        cont = 0
        while valido and cont < len(movimientos):
            mov = movimientos[cont]
            # Averigua el sentido del movimiento y el indice del coche a mover
            adelante = True
            if mov.isupper():
                adelante = False
                ind = ord(mov) - 65
            else:
                ind = ord(mov) - 97
            
            if ind > len(self.nivel)-1:
                print "Movimiento", mov, "imposible. No existe ese coche"
                valido = False
            else:
                if adelante:
                    if self.nivel[ind].orientacion == "H":
                        if not self.comprobarColision(self.nivel[ind].posX + self.nivel[ind].longitud, self.nivel[ind].posY):
                            self.nivel[ind].posX += 1
                        else:
                            print "Movimiento", mov, "imposible por bloqueo"
                            valido = False
                    else:
                        if not self.comprobarColision(self.nivel[ind].posX, self.nivel[ind].posY + self.nivel[ind].longitud):
                            self.nivel[ind].posY += 1
                        else:
                            print "Movimiento", mov, "imposible por bloqueo"
                            valido = False
                else:
                    if self.nivel[ind].orientacion == "H":
                        if not self.comprobarColision(self.nivel[ind].posX - 1, self.nivel[ind].posY):
                            self.nivel[ind].posX -= 1
                        else:
                            print "Movimiento", mov, "imposible por bloqueo"
                            valido = False
                    else:
                        if not self.comprobarColision(self.nivel[ind].posX, self.nivel[ind].posY - 1):
                            self.nivel[ind].posY -= 1
                        else:
                            print "Movimiento", mov, "imposible por bloqueo"
                            valido = False
            if valido: # Si el movimiento es válido, aumenta el contador
                cont += 1 
        self.modificarTablero() # Modifica el tablero según los movimientos elegidos
        return cont # Devuelve el número de movimientos efectuados

    # Comprueba si se produce una colisión en unas coordenadas. True si se produce, False si no
    def comprobarColision(self, x, y):
        colision = False # Por defecto False
        if x > 6 or y > 6 or x < 1 or y < 1: # Comprueba colisión con bordes
            if x != 7 or y != 3: # Comprueba si no colisiona con la salida
                colision = True
        else: # Comprueba colisión con coches
        	for coche in self.nivel:
        		if coche.orientacion == 'H':
        			if y == coche.posY and x >= coche.posX and x < coche.posX + coche.longitud: # Si coinciden las Y y la x a comprobar se encuentra en el intervalo x~x+lon, hay colisión
        				colision = True
        		else:
        			if x == coche.posX and y >= coche.posY and y < coche.posY + coche.longitud: # Si coinciden las X y la y a comprobar se encuentra en el intervalo y~y+lon, hay colisión
        				colision = True
        return colision
    
    # Comprueba si ha acabado el juego. True si acaba, False si no
    def comprobarGameOver(self):
        gameOver = False
        if self.nivel[0].posY == 3 and self.nivel[0].posX + self.nivel[0].longitud - 1 == 7: # Si la parte final del coche se sale del tablero, fin del juego
            self.tablero[2][6] = [ 3*COE + CSO + CONS, 2*" " + "a" + CNS + CNS, 3*COE + CON + CNS ] # Cambia la casilla al acabar
            gameOver = True

        return gameOver
    
# Carga los niveles desde un fichero. Devuelve una lista de niveles
def cargarNiveles(nomFich):
    nivs = []
    try:
        with open(nomFich, "r") as fichero:
            lineas = fichero.read().splitlines()
        n = int(lineas[0])
        cont = 1
        for i in xrange(n):
            x = int(lineas[cont])
            cont += 1
            nivel = []
            letra = 65
            for j in xrange(x):
                lin = lineas[cont]
                nivel.append(Coche(chr(letra), lin[0], lin[1], lin[2], lin[3]))
                cont += 1
                letra += 1
            nivs.append(nivel)
    except IOError:
        print "No existe el archivo niveles.txt"
        nivs = None
    return nivs

# Carga las puntuaciones anteriores del jugador, si existen
def cargarPuntuaciones(nomFich, numnivs):
    punts = []
    try:
        with open(nomFich, "r") as fichero: # Abre el archivo, separa las líneas eliminando saltos de líneas y cierra el archivo
            lineas = fichero.read().splitlines()
        for linea in lineas: # Carga las puntuaciones
            punts.append(int(linea))
    except IOError: # No existe el archivo
        punts = [0] * numnivs # Devuelve una lista vacía
    return punts

# Guarda las puntuaciones del jugador en un archivo
def guardarPuntuaciones(punts, nomFich):
    with open(nomFich, "w") as fichero: # Abre el fichero y escribe los valores de la lista de puntuaciones
        for punt in punts:
            fichero.write(str(punt) + "\n")

# Crea un nuevo juego para el nivel elegido
def nuevoJuego(numniv, nivel, record):
    limpiarPantalla() # Limpia la pantalla
    nummovs = 0 # Pone el contador de movimientos a 0
    tablero = Tablero(nivel) # Crea el tablero de juego
    tablero.mostrarTablero(str(numniv), nummovs, record) # Muestra el tablero inicial
    gameOver = False # Bucle de juego
    while not gameOver:
        movs = raw_input("Movimientos: ")
        if movs.isalpha():
            nummovs += tablero.realizarMovimientos(movs) # Realiza los movimientos e incrementa el contador
            gameOver = tablero.comprobarGameOver()
            limpiarPantalla() # Limpia la pantalla
            tablero.mostrarTablero(str(numniv), nummovs, record) # Muestra el tablero
        elif movs == "":
        	print "Introduce algún movimiento"
        else:
            print "No introduzcas caracteres inválidos"

    return nummovs

# Devuelve el nivel máximo que se puede elegir
def maximoNivel(punts):
	i = 0
	salir = False
	while not salir and i < len(punts):
		if punts[i] == 0:
			salir = True
		else:
			i += 1
	return i+1

# Realiza un limpiado de la pantalla con la orden UNIX "clear"
def limpiarPantalla():
	if limpiadoPantalla: call("clear")

# PROGRAMA PRINCIPAL
def main():
    niveles = cargarNiveles(ficNiv) # Carga los niveles
    if(niveles != None):
        punts = cargarPuntuaciones(ficPun, len(niveles)) # Carga las puntuaciones (si existen)

        niv = 0
        maxniv = maximoNivel(punts)
        # Pide el nivel a cargar
        while niv < 1 or niv > maxniv:
            try:
                niv = int(raw_input("Elija nivel (1-" + str(maxniv) + "): "))
                if niv < 1 or niv > maxniv:
                    print "Elige un nivel válido"
            except:
                print "Eso no es un número."

        salir = False
        while not salir:
            nummovs = nuevoJuego(niv, niveles[niv-1], punts[niv-1]) # Crea un nuevo juego
            print "¡Enhorabuena, ha completado el nivel!\nMovimientos:", nummovs,
            if nummovs < punts[niv-1] or punts[niv-1] == 0: # Nuevo récord
                print "(¡NUEVO RÉCORD!)"
                punts[niv-1] = nummovs # Guarda el record
            else: 
            	print ""
            
            salir2 = False
            while not salir2:
            	elec = raw_input("¿Desea pasar al siguiente nivel? [S/N] > ")
    	        if elec == "S" or elec == "s":
    	            niv += 1
    	            salir2 = True
    	            if niv > len(niveles):
    	                print "Ya no hay más niveles :("
    	        elif elec == "N" or elec == "n":
    	            print "¡Tú te lo pierdes! ;)"
    	            salir2 = salir = True
    	        else:
    	        	print "Perdona no te he entendido"

        guardarPuntuaciones(punts, ficPun) # Guarda los records

try:
    main() # Comienza el programa
except KeyboardInterrupt:
    print "\n\nSaliendo del juego"
except EOFError:
    print "\n\nSaliendo del juego"
except:
    print "\n\nError inesperado. Saliendo del juego"