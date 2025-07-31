import pygame
import sys
import random
import math

# =========================
# INICIALIZACIÓN
# =========================
pygame.init()

# Tamaño de la ventana visible
VENTANA_ANCHO = 1280
VENTANA_ALTO = 720
pantalla = pygame.display.set_mode((VENTANA_ANCHO, VENTANA_ALTO))
pygame.display.set_caption("Escenario con moto y cartas")

# Fondo de 1280x4320 (scroll vertical)
fondo = pygame.image.load("assets/escenario/background.png").convert()
FONDO_ALTO = fondo.get_height()

# Moto
moto_img = pygame.image.load("assets/moto.png").convert_alpha()
moto_rect = moto_img.get_rect(topleft=(600, FONDO_ALTO - moto_img.get_height() - 50))
moto_mask = pygame.mask.from_surface(moto_img)

# Velocidad
velocidad = 10

# Scroll vertical
scroll_y = 0

# =========================
# OBJETOS FÍSICOS
# =========================
pos_agricultores = (0, 100)
pos_ancianos = (VENTANA_ANCHO - 700, 800)
pos_enfermos = (-100, 1500)
pos_familia = (VENTANA_ANCHO - 400, 2000)
pos_soldado = (0, 3000)

objetos = []
for ruta, pos in [
    ("assets/escenario/agricultores.png", pos_agricultores),
    ("assets/escenario/ancianos.png", pos_ancianos),
    ("assets/escenario/enfermos.png", pos_enfermos),
    ("assets/escenario/familia.png", pos_familia),
    ("assets/escenario/soldado.png", pos_soldado)
]:
    img = pygame.image.load(ruta).convert_alpha()
    rect = img.get_rect(topleft=pos)
    mask = pygame.mask.from_surface(img)
    objetos.append((img, rect, mask))

# =========================
# LÓGICA DE CARTAS
# =========================
fuente = pygame.font.SysFont("georgia", 26, bold=True)

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

puntos_cartas = [
    (570, 350),
    (680, 1200),
    (550, 1800),
    (900, 2500),
    (600, 3400), # abajo
]

mostrar_carta = False
texto_actual = ""
puntos = 0
boton_presionado = False
puntos_usados = []
punto_actual = None

# =========================
# FUNCIONES
# =========================

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

    superficies = []
    for linea in lineas:
        superficie = fuente.render(linea, True, color)
        superficies.append(superficie)
    return superficies

def dibujar_carta():
    pantalla.blit(fondo_carta, fondo_carta_rect)

    # Texto centrado con margen y salto de línea
    margen = 40
    lineas_renderizadas = renderizar_texto_multilinea(
        texto_actual, fuente, (0, 0, 0), fondo_carta_rect.width, margen
    )
    alto_total = sum([l.get_height() for l in lineas_renderizadas]) + (len(lineas_renderizadas) - 1) * 5
    y_texto = fondo_carta_rect.centery - alto_total // 2

    for linea in lineas_renderizadas:
        texto_rect = linea.get_rect(center=(fondo_carta_rect.centerx, y_texto))
        pantalla.blit(linea, texto_rect)
        y_texto += linea.get_height() + 5

    # Botones con hover
    mouse_pos = pygame.mouse.get_pos()
    if btn_aceptar_rect.collidepoint(mouse_pos):
        pantalla.blit(btn_aceptar_zoom, btn_aceptar_zoom.get_rect(center=btn_aceptar_rect.center))
    else:
        pantalla.blit(btn_aceptar, btn_aceptar_rect)

    if btn_no_rect.collidepoint(mouse_pos):
        pantalla.blit(btn_no_zoom, btn_no_zoom.get_rect(center=btn_no_rect.center))
    else:
        pantalla.blit(btn_no, btn_no_rect)

# =========================
# LOOP PRINCIPAL
# =========================
clock = pygame.time.Clock()
tiempo = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Clic en botones (con bloqueo tras primer clic)
        if mostrar_carta and not boton_presionado and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if btn_aceptar_rect.collidepoint(event.pos):
                puntos += 100
                mostrar_carta = False
                boton_presionado = True
                if punto_actual and punto_actual not in puntos_usados:
                    puntos_usados.append(punto_actual)
                punto_actual = None

            elif btn_no_rect.collidepoint(event.pos):
                puntos -= 100
                mostrar_carta = False
                boton_presionado = True
                if punto_actual and punto_actual not in puntos_usados:
                    puntos_usados.append(punto_actual)
                punto_actual = None

    # Movimiento solo si no hay carta abierta
    if not mostrar_carta:
        teclas = pygame.key.get_pressed()
        nueva_pos = moto_rect.copy()

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            nueva_pos.y -= velocidad
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            nueva_pos.y += velocidad
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            nueva_pos.x -= velocidad
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            nueva_pos.x += velocidad

        nueva_pos.x = max(0, min(nueva_pos.x, VENTANA_ANCHO - moto_img.get_width()))
        nueva_pos.y = max(0, min(nueva_pos.y, FONDO_ALTO - moto_img.get_height()))

        colision = False
        for obj_img, obj_rect, obj_mask in objetos:
            offset = (nueva_pos.x - obj_rect.x, nueva_pos.y - obj_rect.y)
            if obj_mask.overlap(moto_mask, offset):
                colision = True
                break

        if not colision:
            moto_rect = nueva_pos

        # Verificar si la moto está cerca de un punto NO USADO
        for punto in puntos_cartas:
            if punto in puntos_usados:
                continue

            distancia = pygame.Vector2(moto_rect.center).distance_to(punto)
            if distancia < 50:
                texto_actual = random.choice(textos_cartas)
                mostrar_carta = True
                boton_presionado = False
                punto_actual = punto
                break

    # Scroll centrado
    scroll_y = max(0, min(FONDO_ALTO - VENTANA_ALTO, moto_rect.centery - VENTANA_ALTO // 2))

    # Dibujar fondo
    pantalla.blit(fondo, (0, -scroll_y))
    for obj_img, obj_rect, _ in objetos:
        pantalla.blit(obj_img, (obj_rect.x, obj_rect.y - scroll_y))

    # Dibujar puntos flotantes
    for punto in puntos_cartas:
        if punto in puntos_usados:
            continue  # no mostrar los ya usados
        flotacion = math.sin(tiempo + punto[1] * 0.01) * 5
        x, y = punto
        pygame.draw.circle(pantalla, (255, 255, 255), (x, int(y - scroll_y + flotacion)), 10)

    # Dibujar moto
    pantalla.blit(moto_img, (moto_rect.x, moto_rect.y - scroll_y))

    # Mostrar puntos
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, (0, 0, 0))
    pantalla.blit(texto_puntos, (20, 20))

    # Mostrar carta si está activa
    if mostrar_carta:
        dibujar_carta()

    pygame.display.flip()
    tiempo += 0.05
    clock.tick(60)
