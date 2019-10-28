# !/usr/bin/env python
# -*- encoding=utf-8 -*-

# AUTORES:
#	ABEL HERRERO GÓMEZ
# 	JORGE SAN JOSÉ LORZA

import pygtk
pygtk.require("2.0")
import gtk
import random # Números aleatorios

# Ficheros
ficNiveles = "niveles.txt"					# Fichero que contiene los niveles
ficRecords = "records.txt"					# Fichero que contiene los records
# Imágenes (rutas al archivo)
pathImages = "images/"
imgAsfalto = "asfalto.png"
wally = "verdeh.png" 						# ¡LIBERAD A WALLY!
img2H = ["rojoh.png", "azulh.png", "amarilloh.png"] # Coches horizontales de largo 2
img3H = ["camiongrih.png", "camionverh.png", "limublah.png", "limunegh.png"] # Coches horizontales de largo 3
img2V = ["rojov.png", "azulv.png", "amarillov.png"] # Coches verticales de largo 2
img3V = ["camiongriv.png", "camionverv.png", "limublav.png", "limunegv.png"] # Coches verticales de largo 3
imgRestart = "restart.png"					# Icono de reinicio
imgExit = "exit.png"						# Icono de salida
# Pantalla
TAM = 6										# Tamaño del tablero
ALTOMENU = 50								# Altura y margen del menú
MARGENMENU = 3
ALTO, ANCHO = 65, 65 						# Alto y ancho en píxeles de una sola casilla
MAXX, MAXY = ANCHO * TAM, ALTO * TAM		# Máximos y mínimos de las variables de pantalla
MINX, MINY = 0, 0
NIVSFILA = 5								# Numero de niveles por fila
# Colores
clDisponible = "#00E251"
clBloqueado = "#A9A9A9"
clTexto = "#000000"
clCreditos = "#A1A1A1"
# Cadenas de texto
stMovs = "MOVIMIENTOS: "
stRec = "RÉCORD: "
stNiv = "NIVEL "
stTitulo = "¡DESBLOQUÉAME!"
stElegir = "ELIGE UN NIVEL"
stCreditos = "By: Abel Herrero &amp; Jorge San José"

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
                c = Coche(chr(letra), lin[0], lin[1], lin[2], lin[3])
                if j == 0: # ¡WALLY!
                	path = wally
            	else:
	                if c.orientacion == "H":
	                	if c.longitud == 2: path = random.choice(img2H)
	                	elif c.longitud == 3: path = random.choice(img3H)
	                else:
	                	if c.longitud == 2: path = random.choice(img2V)
	                	elif c.longitud == 3: path = random.choice(img3V)
                c.add(gtk.image_new_from_file(pathImages + path))
                nivel.append(c)
                cont += 1
                letra += 1
            nivs.append(nivel)
    except IOError:
        print "No existe el archivo", nomFich
        nivs = None
    return nivs
# Carga las puntuaciones anteriores del jugador, si existen
def cargarRecords(numnivs):
	punts = []
	try:
		with open(ficRecords, "r") as fichero: # Abre el archivo, separa las líneas eliminando saltos de líneas y cierra el archivo
			lineas = fichero.read().splitlines()
		for linea in lineas: # Carga las puntuaciones
			punts.append(int(linea))
	except IOError: # No existe el archivo
		punts = [0] * numnivs # Devuelve una lista vacía
	return punts
# Guarda las puntuaciones del juego en un archivo
def guardarRecords(punts):
    with open(ficRecords, "w") as fichero: # Abre el fichero y escribe los valores de la lista de puntuaciones
        for punt in punts: fichero.write(str(punt) + "\n")

class Desbloqueame:
	# Constructor
	def __init__(self, ficheroNiveles):
	# Configura las ventanas
		self.ventana = gtk.Window()
		self.ventana.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
		self.ventana.set_title("Desbloquéame")
		self.ventana.set_resizable(False)
		self.ventana.set_size_request(MAXX, MAXY + 2*MARGENMENU + ALTOMENU)
		self.ventana.connect("destroy", gtk.main_quit)
		# Layout vertical
		self.vpaned = gtk.VBox()
		# Crea el tablero
		self.tablero = gtk.Fixed()
		self.tablero.set_size_request(MAXX, MAXY)		# Configura el tamaño del tablero
		self.vpaned.add(self.tablero)
		# Crea el menú inferior
		self.menu = gtk.Table(2, 2, True)
		self.menu.set_size_request(MAXX - 4 * MARGENMENU, ALTOMENU)
		self.menu.set_border_width(MARGENMENU)
			# Textos del menú inferior (vacíos por defecto)
		self.tvNivel = gtk.Label()
		self.tvMovs = gtk.Label()
		self.tvRec = gtk.Label()
		self.menu.attach(self.tvNivel, 0, 2, 0, 1) # Ocupa la parte superior
		self.menu.attach(self.tvMovs, 0, 1, 1, 2)  # Inferior izquierda
		self.menu.attach(self.tvRec, 1, 2, 1, 2)   # Inferior derecha
		eb = gtk.EventBox()
		eb.add(self.menu)
		eb.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(clDisponible))
		self.vpaned.add(eb)
		self.ventana.show()
	# Configura los datos
		self.numNivel = 0									# Contador de niveles
		self.niveles = cargarNiveles(ficheroNiveles) 		# Lista de niveles
		self.nivelactual = self.niveles[0]					# Asigna el primer nivel
		self.records = cargarRecords(len(self.niveles))		# Carga las puntuaciones
	# Comienza el juego
		self.menuPrincipal()

	# Muestra el menú principal
	def menuPrincipal(self):
		ch = self.ventana.get_children()
		if len(ch) != 0:
			self.ventana.remove(ch[0]) # Solo tiene un hijo

		self.menuPri = gtk.Table(4, 1, False)
		tvTitulo = gtk.Label()
		tvTitulo.set_markup('<span background="' + clDisponible + '" foreground="' + clTexto + '" size="20000"><b><i><u>' + stTitulo + '</u></i></b></span>')
		tvElegir = gtk.Label()
		tvElegir.set_markup('<span foreground="' + clTexto + '" size="15000"><b>' + stElegir + '</b></span>')
		self.menuPri.attach(tvTitulo, 0, 1, 0, 1, yoptions = gtk.SHRINK, ypadding = ALTOMENU/2)
		self.menuPri.attach(tvElegir, 0, 1, 1, 2, yoptions = gtk.SHRINK, ypadding = ALTOMENU/2)

		# Halla el ultimo nivel jugable (el primero no hecho)
		found = False
		ultNivel = 0
		while not found and ultNivel < len(self.records):
			if self.records[ultNivel] == 0:
				found = True
			else: ultNivel += 1

		numFilas = len(self.niveles) / NIVSFILA # Número de filas
		if numFilas == 0: numFilas = 1
		# Tabla de niveles
		tablaNivs = gtk.Table(numFilas, NIVSFILA, homogeneous=False) # Tabla con los niveles
		tablaNivs.set_row_spacings(10)
		tablaNivs.set_col_spacings(10)
		tablaNivs.set_border_width(10)
		# Añade los niveles
		x, y = 0, 0
		for i in xrange(len(self.niveles)): 
			b = gtk.Button()
			num = gtk.Label()
			num.set_markup('<span foreground="' + clTexto + '" size="15000"><b>' + str(i+1) + '</b></span>')
			b.add(num)
			b.nivel = i
			b.set_focus_on_click(False)
			if i <= ultNivel:
				b.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(clDisponible))
				b.connect("clicked", self.onItemClick)
			else:
				b.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(clBloqueado))
			tablaNivs.attach(b, x, x+1, y, y+1)
			x += 1
			if x == NIVSFILA: x = 0; y += 1
		self.menuPri.attach(tablaNivs, 0, 1, 2, 3)

		tvCreditos = gtk.Label()
		tvCreditos.set_markup('<span foreground="' + clCreditos + '" size="6000"><b><i><u>' + stCreditos + '</u></i></b></span>')
		self.menuPri.attach(tvCreditos, 0, 1, 3, 4)

		self.menuPri.show_all()
		self.ventana.add(self.menuPri)
	# Manejador de evento
	def onItemClick(self, boton):		
		# Crea un nuevo juego
		self.numNivel = boton.nivel
		self.nuevoJuego()
	# Crea un nuevo juego
	def nuevoJuego(self):
		ch = self.ventana.get_children()
		if len(ch) != 0:
			self.ventana.remove(ch[0]) # Solo tiene un hijo

		for ch in self.tablero.get_children():
			self.tablero.remove(ch)
		self.ventana.add(self.vpaned)

		self.numMovs = 0 								# Reinicia el contador de movimientos
		self.nivelactual = self.niveles[self.numNivel] 	# Obtiene el nivel actual
		# Configura el fondo del tablero
		fondo = gtk.image_new_from_file(pathImages + imgAsfalto)
		self.tablero.put(fondo, 0, 0)	
		# Configura los textos mostrados
		self.tvNivel.set_markup('<span foreground="' + clTexto + '" size="15000"><b>' + stNiv + str(self.numNivel+1) + '</b></span>')
		self.tvMovs.set_markup('<span foreground="' + clTexto + '" size="13000"><b>' + stMovs + str(self.numMovs) + '</b></span>')
		self.tvRec.set_markup('<span foreground="' + clTexto + '" size="13000"><b>' + stRec + str(self.records[self.numNivel]) + '</b></span>')
		# Añade los coches
		for coche in self.nivelactual:
			self.tablero.put(coche, (coche.posX-1) * ANCHO, (coche.posY-1) * ALTO) # Coloca los coches	
		# Añade los botones de restart y exit
		restart = gtk.EventBox()
		restart.set_visible_window(False)
		restart.set_border_width(2)
		restart.add(gtk.image_new_from_file(pathImages + imgRestart))
		restart.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		restart.connect("button_press_event", lambda w, e: self.nuevoJuego())
		exit = gtk.EventBox()
		exit.set_visible_window(False)
		exit.set_border_width(2)
		exit.add(gtk.image_new_from_file(pathImages + imgExit))
		exit.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		exit.connect("button_press_event", lambda w, e: self.menuPrincipal())		# Vuelve al menú principal
		botones = gtk.HBox()
		botones.add(restart)
		botones.add(exit)
		self.tablero.put(botones, MAXX - 20*2 - 8, 0)
		self.vpaned.show_all()						# Muestra todos los elementos del tablero
	# Obtiene y acumula los movimientos realizados
	def sumarMovimientos(self, xi, yi, xn, yn):
		movsX = abs(xn - xi) / ANCHO # Numero de movimientos en el eje X
		movsY = abs(yn - yi) / ALTO # Numero de movimientos en el eje Y
		self.numMovs += movsX + movsY # Uno de los dos es 0 siempre
		self.tvMovs.set_markup('<span foreground="' + clTexto + '" size="13000"><b>' + stMovs + str(self.numMovs) + '</b></span>') # Crea el texto con estilo
	# Finaliza un juego
	def gameOver(self):
		mensaje = gtk.MessageDialog(type = gtk.MESSAGE_QUESTION, buttons = gtk.BUTTONS_YES_NO, flags = gtk.DIALOG_MODAL)
		mensaje.set_title("¡Has ganado en " + str(self.numMovs) + " movimientos!")
		stMensaje = "¿Deseas pasar al siguiente nivel?"
		# Comprueba si ha habido record
		if self.numMovs < self.records[self.numNivel] or self.records[self.numNivel] == 0:
			self.records[self.numNivel] = self.numMovs # Guarda el record
			stMensaje = "¡NUEVO RECORD!\n" + stMensaje # Añade el mensaje de record
			guardarRecords(self.records)

		mensaje.set_markup(stMensaje)
		eleccion = mensaje.run()
		mensaje.destroy()
		if eleccion == gtk.RESPONSE_YES:
			if self.numNivel + 1 >= len(self.niveles): # No hay más niveles
				mensaje = gtk.MessageDialog(type = gtk.MESSAGE_WARNING, buttons = gtk.BUTTONS_OK, flags = gtk.DIALOG_MODAL)
				mensaje.set_markup("Lo siento, no hay más niveles :(")
				mensaje.run()
				mensaje.destroy()
				# Sale al menú
				return gtk.FALSE
			else:
				return gtk.TRUE
		else:
			return gtk.FALSE

# Objeto Coche
class Coche(gtk.EventBox): 
	# Constructor: nombre, orientación, coordenada_X, coordenada_Y, longitud
	def __init__(self, nom, ori, x, y, lon):
		gtk.EventBox.__init__(self) 	# Inicializa el Widget
		self.set_visible_window(False)  # Para que no se vea el EventBox
		self.nombre = nom 				# Identificador del coche
		self.orientacion = ori 			# Orientación: H (horizontal) o V (vertical)
		self.posX = int(x)				# Coordenada X en el tablero (1~6)
		self.posY = int(y) 				# 			 Y en el tablero (1~6)
		self.longitud = int(lon) 		# Longitud en casillas del coche
		self.grabbed = False 			# Flag de agarrado
		# Activa y conecta los eventos a utilizar
		self.set_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK)
		self.connect("button_press_event", self.on_press)		# Hacer click
		self.connect("button_release_event", self.on_release) 	# Soltar click
		self.connect("motion_notify_event", self.on_motion)		# Mover por encima
	
	# Manejador de evento: al pulsar sobre un coche
	def on_press(self, wid, event, data = None):
		self.grabbed = True 									# Se ha "agarrado" el coche
		self.x0, self.y0 = int(event.x_root), int(event.y_root) # Coordenadas del click
		self.rect = wid.get_allocation() 						# Area ocupada por el EventBox
		self.xi, self.yi = self.rect.x, self.rect.y 			# Coordenadas originales del coche
		self.dx, self.dy = 0, 0 								# Incremento/Decremento de coordenadas
		self.bZona = None 										# Zona de bloqueo
		self.blocked = False 									# Flag de bloqueo (con otros coches)

	# Manejador de evento: al soltar un coche
	def on_release(self, wid, event, data = None):
		self.grabbed = False 								# Se ha soltado el coche
		# Sistema de recolocación
		dims = wid.get_allocation() 						# Obtiene la posición final del contenedor
		newX = int(round(float(dims.x) / ANCHO)) * ANCHO 	# Recoloca en la casilla X más cercana
		newY = int(round(float(dims.y) / ALTO)) * ALTO 		# Recoloca en la casilla Y más cercana
		juego.tablero.move(wid, newX, newY)
		juego.sumarMovimientos(self.xi, self.yi, newX, newY) # Obtiene los movimientos realizados y los suma
		return gtk.TRUE

	# Manejador de evento: al mover sobre un coche
	def on_motion(self, wid, event, data = None):
		if not self.grabbed: # Si no se está agarrando ningún coche, se ignora
			return gtk.FALSE

		# Obtiene las coordenadas relativas del coche y el click
		if wid.orientacion == "H": self.dx = int(event.x_root) - self.x0
		else: self.dy = int(event.y_root) - self.y0
		coordX, coordY = self.xi + self.dx, self.yi + self.dy
		
		self.rect = wid.get_allocation() # Área ocupada por el EventBox
		# Comprueba colisiones con los bordes de la ventana
		if coordX < MINX: coordX = MINX
		elif coordX + self.rect.width > MAXX:
			if wid.nombre == "A":
				if self.rect.x + (self.rect.width/2) >= MAXX:
					juego.tablero.move(wid, MAXX - (self.rect.width/2), coordY)
					juego.sumarMovimientos(self.xi, self.yi, self.rect.x, self.yi)
					if juego.gameOver() == gtk.TRUE: # Muestra el cartel de Game Over
						juego.numNivel += 1
						juego.nuevoJuego()
					else:
						juego.menuPrincipal()
					return gtk.TRUE
			else: coordX = MAXX - self.rect.width
		elif coordY < MINY: 
			coordY = MINY
		elif coordY + self.rect.height >= MAXY:
			coordY = MAXY - self.rect.height

		# Comprueba colisiones con otros coches (con su EventBox)
		cont = 0
		while not self.blocked and cont < len(juego.nivelactual):
			coche = juego.nivelactual[cont]
			if coche != wid: # Ignora el coche agarrado
				zona = coche.get_allocation() # Recuadro del coche a comprobar
				if coordX < zona.x + zona.width and coordX + self.rect.width > zona.x and coordY < zona.y + zona.height and coordY + self.rect.height > zona.y:
					self.blocked = True # Activa el bloqueo del coche
					self.bZona = zona # Recuadro del bloqueo
			cont += 1

		# Manejo de bloqueos
		if self.blocked:
			if wid.orientacion == "H":
				if self.bZona.x > self.xi: # Se mueve a la derecha
					if coordX + self.rect.width < self.bZona.x: self.blocked = False
					else: juego.tablero.move(wid, self.bZona.x - self.rect.width, coordY)
				elif self.bZona.x < self.xi: # Se mueve a la izquierda
					if coordX > self.bZona.x + self.bZona.width: self.blocked = False
					else: juego.tablero.move(wid, self.bZona.x + self.bZona.width, coordY)
				else: self.blocked = False
			else:
				if self.bZona.y > self.yi: # Se mueve hacia abajo
					if coordY + self.rect.height < self.bZona.y: self.blocked = False
					else: juego.tablero.move(wid, coordX, self.bZona.y - self.rect.height)
				elif self.bZona.y < self.yi: # Se mueve hacia arriba
					if coordY > self.bZona.y + self.bZona.height: self.blocked = False
					else: juego.tablero.move(wid, coordX, self.bZona.y + self.bZona.height)
				else: self.blocked = False

		if not self.blocked: juego.tablero.move(wid, coordX, coordY) # Si no está bloqueado, mueve el coche
		return gtk.TRUE

juego = Desbloqueame(ficNiveles) # Crea una nueva partida
gtk.main()