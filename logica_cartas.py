import pygame
import sys
import random
from escenario import moto_rect

# Inicializar Pygame
pygame.init()

# Tamaño ventana
VENTANA_ANCHO = 1280
VENTANA_ALTO = 720
pantalla = pygame.display.set_mode((VENTANA_ANCHO, VENTANA_ALTO))
pygame.display.set_caption("Lógica de Cartas")

# Fuente
fuente = pygame.font.SysFont("georgia", 26, bold=True)

# Cargar imágenes
fondo_carta = pygame.image.load("assets/escenario/base_carta.png").convert_alpha()
fondo_carta_rect = fondo_carta.get_rect(center=(VENTANA_ANCHO // 2, VENTANA_ALTO // 2))

btn_aceptar = pygame.image.load("assets/escenario/1.png").convert_alpha()
btn_no = pygame.image.load("assets/escenario/2.png").convert_alpha()

btn_aceptar_zoom = pygame.transform.scale_by(btn_aceptar, 1.1)
btn_no_zoom = pygame.transform.scale_by(btn_no, 1.1)

btn_aceptar_rect = btn_aceptar.get_rect(center=(VENTANA_ANCHO // 2 - 150, fondo_carta_rect.bottom - 60))
btn_no_rect = btn_no.get_rect(center=(VENTANA_ANCHO // 2 + 150, fondo_carta_rect.bottom - 60))

textos_cartas = [
    "Una familia necesita arroz y agua urgentemente.",
    "Un grupo de ancianos clama por ayuda alimentaria.",
    "Un soldado vigila, pero no ha comido en días.",
    "Un agricultor pide fertilizante y una ración.",
    "Un enfermo necesita comida blanda y medicina."
]

# Puntos de activación (manual)
puntos_disparo = [
    (100, 150),
    (1100, 850),
    (100, 1900),
    (1100, 2700),
    (100, 3800),
]

# Seguimiento de estado
mostrar_carta = False
texto_actual = ""
puntos = 0
boton_presionado = False
puntos_usados = []  # Guardamos los puntos ya utilizados
punto_actual = None  # Referencia al punto que activó la carta

clock = pygame.time.Clock()

# -----------------------
# Renderizado de texto
# -----------------------
def renderizar_texto_multilinea(texto, fuente, color, ancho_maximo, margen_x):
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        test_linea = linea_actual + palabra + " "
        if fuente.size(test_linea)[0] < ancho_maximo - 2 * margen_x:
            linea_actual = test_linea
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "
    lineas.append(linea_actual.strip())

    superficies = [fuente.render(linea, True, color) for linea in lineas]
    return superficies

# -----------------------
# Dibuja carta en pantalla
# -----------------------
def dibujar_carta():
    pantalla.blit(fondo_carta, fondo_carta_rect)

    margen = 40
    lineas_renderizadas = renderizar_texto_multilinea(
        texto_actual, fuente, (0, 0, 0), fondo_carta_rect.width, margen
    )

    alto_total = sum([linea.get_height() for linea in lineas_renderizadas]) + (len(lineas_renderizadas) - 1) * 5
    y_texto = fondo_carta_rect.centery - alto_total // 2

    for linea in lineas_renderizadas:
        texto_rect = linea.get_rect(center=(fondo_carta_rect.centerx, y_texto))
        pantalla.blit(linea, texto_rect)
        y_texto += linea.get_height() + 5

    # Botones con efecto hover
    mouse_pos = pygame.mouse.get_pos()
    if btn_aceptar_rect.collidepoint(mouse_pos):
        pantalla.blit(btn_aceptar_zoom, btn_aceptar_zoom.get_rect(center=btn_aceptar_rect.center))
    else:
        pantalla.blit(btn_aceptar, btn_aceptar_rect)

    if btn_no_rect.collidepoint(mouse_pos):
        pantalla.blit(btn_no_zoom, btn_no_zoom.get_rect(center=btn_no_rect.center))
    else:
        pantalla.blit(btn_no, btn_no_rect)

# -----------------------
# Bucle principal
# -----------------------
while True:
    pantalla.fill((240, 240, 240))  # Fondo neutro

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Clic en botones
        if mostrar_carta and not boton_presionado and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if btn_aceptar_rect.collidepoint(mouse_pos):
                puntos += 100
                boton_presionado = True
                mostrar_carta = False
                if punto_actual and punto_actual not in puntos_usados:
                    puntos_usados.append(punto_actual)
                punto_actual = None  # limpiar

            elif btn_no_rect.collidepoint(mouse_pos):
                puntos -= 100
                boton_presionado = True
                mostrar_carta = False
                if punto_actual and punto_actual not in puntos_usados:
                    puntos_usados.append(punto_actual)
                punto_actual = None  # limpiar

    # Mostrar puntos actuales
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, (0, 0, 0))
    pantalla.blit(texto_puntos, (20, 20))

    # Verificar si la moto está cerca de un punto NO USADO
    if not mostrar_carta:
        for punto in puntos_disparo:
            if punto in puntos_usados:
                continue  # Saltar si ya se usó

            distancia = pygame.Vector2(moto_rect.center).distance_to(punto)
            if distancia < 50:
                punto_actual = punto  # guardar el punto actual
                texto_actual = random.choice(textos_cartas)
                mostrar_carta = True
                boton_presionado = False
                break

    # Mostrar carta si corresponde
    if mostrar_carta:
        dibujar_carta()

    pygame.display.flip()
    clock.tick(60)
