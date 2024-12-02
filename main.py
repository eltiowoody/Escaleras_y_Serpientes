import os
import pygame
import random

# Inicialización de Pygame
pygame.init()

# Crear ventana
pygame.display.set_caption('Escaleras y Serpientes con arthas')
ANCHO, ALTO = 600, 450  # Dimensiones de la pantalla
screen = pygame.display.set_mode((ANCHO, ALTO))
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Constantes del tablero
NUMERO_COLUMNAS = 10
NUMERO_FILAS = 10
TAMANIO_CASILLA = min(ANCHO // NUMERO_COLUMNAS, ALTO // NUMERO_FILAS)

# Diccionario de serpientes y escaleras
serpientes_y_escaleras = {
    # Escaleras:
    3: 39,
    14: 35,
    31: 70,
    44: 65,
    47: 86,
    63: 83,
    59: 80,
    72: 91,

    # Serpientes:
    98: 64,
    93: 69,
    90: 33,
    79: 42,
    54: 37,
    40: 4,
    30: 8,
}

# Variables del jugador
posicion_jugador = 1
numero_dado = None
movimiento_habilitado = False

# Definir el rectángulo del dado
dado_rect = pygame.Rect(ANCHO - 100, ALTO - 100, 50, 50)

# Cargar la ficha del jugador
ficha_jugador = pygame.image.load(os.path.join('data', 'ficha.JPG')).convert_alpha()
ficha_jugador = pygame.transform.scale(ficha_jugador, (TAMANIO_CASILLA // 2, TAMANIO_CASILLA // 2))

# Cargar la imagen para la parte derecha
imagen_derecha = pygame.image.load(os.path.join('data', 'imagen_derecha.jpg')).convert()
imagen_derecha = pygame.transform.scale(imagen_derecha, (ANCHO // 3, ALTO))  # Escalamos la imagen para ocupar el espacio de la derecha

# Función para lanzar el dado
def lanzar_dado():
    return random.randint(1, 6)

# Función para dibujar el dado
def dibujar_dado(x, y, numero):
    pygame.draw.rect(screen, BLACK, (x, y, 50, 50), 3)  # Contorno del dado
    font = pygame.font.Font(None, 30)  # Fuente del texto
    text = font.render(str(numero), True, WHITE)  # Número del dado
    text_width, text_height = text.get_size()
    text_x = x + (50 - text_width) // 2  # Centrar horizontalmente
    text_y = y + (50 - text_height) // 2  # Centrar verticalmente
    # Dibujar el texto
    screen.blit(text, (text_x, text_y))

# Función para dibujar la ficha del jugador
def dibujar_ficha(x, y):
    ficha_x = x + (TAMANIO_CASILLA - ficha_jugador.get_width()) // 2
    ficha_y = y + (TAMANIO_CASILLA - ficha_jugador.get_height()) // 2
    screen.blit(ficha_jugador, (ficha_x, ficha_y))

# Función para calcular la posición en pantalla de una casilla
def calcular_posicion(posicion):
    fila = (posicion - 1) // NUMERO_COLUMNAS
    columna = (posicion - 1) % NUMERO_COLUMNAS
    if fila % 2 == 1:  # Si es una fila impar, invertir la dirección
        columna = NUMERO_COLUMNAS - 1 - columna
    return columna * TAMANIO_CASILLA, (NUMERO_FILAS - 1 - fila) * TAMANIO_CASILLA

# Función para mover al jugador
def mover_jugador(posicion, numero_dado):
    nueva_posicion = posicion + numero_dado
    if nueva_posicion > 100:
        nueva_posicion = 100  # Limitar al máximo de casillas
    if nueva_posicion in serpientes_y_escaleras:
        nueva_posicion = serpientes_y_escaleras[nueva_posicion]  # Mover según serpiente/escalera
    return nueva_posicion

# Función para manejar el clic en el dado
def manejar_click(event):
    global numero_dado, movimiento_habilitado
    if dado_rect.collidepoint(event.pos) and not movimiento_habilitado:
        numero_dado = lanzar_dado()
        movimiento_habilitado = True

# Función para dibujar el tablero
def dibujar_tablero():
    for fila in range(NUMERO_FILAS):
        for columna in range(NUMERO_COLUMNAS):
            color = WHITE if (fila + columna) % 2 == 0 else BLACK
            pygame.draw.rect(
                screen, color,
                (columna * TAMANIO_CASILLA, fila * TAMANIO_CASILLA, TAMANIO_CASILLA, TAMANIO_CASILLA)
            )

# Bucle principal del juego
running = True
while running:
    screen.fill(WHITE)  # Limpiar la pantalla

    # Dibujar la parte derecha con la imagen
    screen.blit(imagen_derecha, (ANCHO - imagen_derecha.get_width(), 0))  # Coloca la imagen a la derecha

    # Dibujar tablero y fichas
    fondo = pygame.image.load(os.path.join('data', 'fondo.jpeg')).convert()
    screen.blit(fondo, ((450-452) / 2, (452-450) / 2))
    x, y = calcular_posicion(posicion_jugador)
    dibujar_ficha(x, y)
    dibujar_dado(dado_rect.x, dado_rect.y, numero_dado if numero_dado else "Play")

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            manejar_click(event)

    # Actualizar posición del jugador si se lanzó el dado
    if movimiento_habilitado:
        posicion_jugador = mover_jugador(posicion_jugador, numero_dado)
        if posicion_jugador == 100:  # Si el jugador alcanza la meta
            print("¡arthas consiguió la Frostmourne!")
            running = False
        movimiento_habilitado = False

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(30)  # Controlar la velocidad del juego

# Cerrar Pygame
pygame.quit()
