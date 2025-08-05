import pygame
import sys
import random
import math
from npc_rata import Rata
from resultado import mostrar_resultado

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

# Ratas
CANTIDAD_RATAS = 20  # ← Podés cambiarlo
ratas = []
for _ in range(CANTIDAD_RATAS):
    x = random.randint(100, VENTANA_ANCHO - 100)
    y = random.randint(500, FONDO_ALTO - 500)
    ratas.append(Rata(x, y))


# Moto
moto_img = pygame.image.load("assets/moto.png").convert_alpha()
moto_rect = moto_img.get_rect(topleft=(600, FONDO_ALTO - moto_img.get_height() - 50))
moto_mask = pygame.mask.from_surface(moto_img)

#Emojis
emoji_alta = pygame.image.load("assets/emoji_alta.png").convert_alpha()
emoji_alta = pygame.transform.smoothscale(emoji_alta, (80, 80))
emoji_media = pygame.image.load("assets/emoji_media.png").convert_alpha()
emoji_media = pygame.transform.smoothscale(emoji_media, (80, 80))
emoji_baja = pygame.image.load("assets/emoji_baja.png").convert_alpha()
emoji_baja = pygame.transform.smoothscale(emoji_baja, (80, 80))

#Flecha
flecha_img = pygame.image.load("assets/flecha_atras.png").convert_alpha()
flecha_img = pygame.transform.scale(flecha_img, (40, 40))  # tamaño real deseado
flecha_rect = flecha_img.get_rect(topleft=(5, 5))  # posición arriba a la izquierda


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

# Parte de abajo del escenario:
pos_agricultores_2 = (0, 4100)
pos_ancianos_2 = (VENTANA_ANCHO - 700, 4800)
pos_enfermos_2 = (-100, 5500)
pos_familia_2 = (VENTANA_ANCHO - 400, 6000)
pos_soldado_2 = (0, 7000)


objetos = []
for ruta, pos in [
    ("assets/escenario/agricultores.png", pos_agricultores),
    ("assets/escenario/ancianos.png", pos_ancianos),
    ("assets/escenario/enfermos.png", pos_enfermos),
    ("assets/escenario/familia.png", pos_familia),
    ("assets/escenario/soldado.png", pos_soldado),

    # Parte inferior del mapa
    ("assets/escenario/agricultores.png", pos_agricultores_2),
    ("assets/escenario/ancianos.png", pos_ancianos_2),
    ("assets/escenario/enfermos.png", pos_enfermos_2),
    ("assets/escenario/familia.png", pos_familia_2),
    ("assets/escenario/soldado.png", pos_soldado_2)
]:
    img = pygame.image.load(ruta).convert_alpha()
    rect = img.get_rect(topleft=pos)
    mask = pygame.mask.from_surface(img)
    objetos.append((img, rect, mask))

# =========================
# LÓGICA DE CARTAS
# =========================
fuente = pygame.font.SysFont("georgia", 32, bold=True)

fondo_carta = pygame.image.load("assets/escenario/base_carta.png").convert_alpha()
fondo_carta_rect = fondo_carta.get_rect(center=(VENTANA_ANCHO // 2, VENTANA_ALTO // 2))

btn_aceptar = pygame.image.load("assets/escenario/1.png").convert_alpha()
btn_no = pygame.image.load("assets/escenario/2.png").convert_alpha()

btn_aceptar_zoom = pygame.transform.scale_by(btn_aceptar, 1.3)
btn_no_zoom = pygame.transform.scale_by(btn_no, 1.3)
0
btn_aceptar_rect = btn_aceptar.get_rect(center=(VENTANA_ANCHO // 2 - 90, fondo_carta_rect.bottom - 200))
btn_no_rect = btn_no.get_rect(center=(VENTANA_ANCHO // 2 + 90, fondo_carta_rect.bottom - 200))

eventos_cartas = [
    {
        "pos": (570, 350),
        "mensaje": "Un agricultor pide fertilizante y una ración."
    },
    {
        "pos": (680, 1200),
        "mensaje": "Un grupo de ancianos clama por ayuda alimentaria."
    },
    {
        "pos": (550, 1800),
        "mensaje": "Un enfermo necesita comida blanda y medicina."
    },
    {
        "pos": (850, 2500),
        "mensaje": "Una familia necesita arroz y agua urgentemente."
    },
    {
        "pos": (600, 3400),
        "mensaje": "Un soldado vigila, pero no ha comido en días."
    },

    # Parte inferior (duplicado)
    {"pos": (570, 4350), "mensaje": "Otro agricultor llegó tras caminar horas pidiendo riego y pan."},
    {"pos": (680, 5200), "mensaje": "Ancianos recién llegados piden ayuda desesperadamente."},
    {"pos": (550, 5800), "mensaje": "Una mujer enferma suplica por algo caliente para comer."},
    {"pos": (850, 6500), "mensaje": "Otra familia desplazada busca apoyo con alimentos."},
    {"pos": (600, 7400), "mensaje": "Un soldado herido implora ayuda mientras patrulla."}
]
mostrar_bienvenida = True
mostrar_carta = False
texto_actual = ""
puntos = 0
estabilidad = 100
boton_presionado = False
puntos_usados = []
punto_actual = None


# Estados de los grupos (todos comienzan vivos)
estado_familias = "vivo"
estado_soldados = "vivo"
estado_agricultores = "vivo"
estado_ancianos = "vivo"
estado_enfermos = "vivo"
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
    # Dimensiones de la caja estilo carta
    ancho_carta = 550
    alto_carta = 300
    x_carta = (VENTANA_ANCHO - ancho_carta) // 2
    y_carta = (VENTANA_ALTO - alto_carta) // 2

    # Fondo oscuro translúcido
    overlay = pygame.Surface((ancho_carta, alto_carta), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))  # negro con transparencia
    pantalla.blit(overlay, (x_carta, y_carta))

    # Texto centrado
    fuente_titulo = pygame.font.SysFont("georgia", 30, bold=True)
    lineas = renderizar_texto_multilinea(texto_actual, fuente_titulo, (255, 255, 255), ancho_carta - 20, 20)
    alto_total = sum([linea.get_height() for linea in lineas]) + (len(lineas) - 1) * 6
    y_texto = y_carta + 60

    for linea in lineas:
        rect = linea.get_rect(center=(VENTANA_ANCHO // 2, y_texto))
        pantalla.blit(linea, rect)
        y_texto += linea.get_height() + 6

    # Botones (manteniendo sus rects actuales)
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

def mostrar_menu():
    background_menu = pygame.image.load("assets/presentacion1.png").convert()
    boton_jugar = pygame.image.load("assets/boton_jugar.png").convert_alpha()
    boton_jugar = pygame.transform.smoothscale(boton_jugar, (190, 80))
    boton_hover = pygame.transform.smoothscale(boton_jugar, (210, 90))
    boton_rect = boton_jugar.get_rect(center=(VENTANA_ANCHO - 150, VENTANA_ALTO - 60))
    titulo_img = pygame.image.load("assets/titulo.png").convert_alpha()
    titulo_img = pygame.transform.smoothscale(titulo_img, (750, 445))
    titulo_rect = titulo_img.get_rect(center=(VENTANA_ANCHO // 2 + 50, 140))

    pygame.mixer.music.load("assets/musica_menu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, start=5.0)

    en_menu = True
    while en_menu:
        pantalla.blit(background_menu, (0, 0))
        pantalla.blit(titulo_img, titulo_rect)

        mouse_pos = pygame.mouse.get_pos()
        if boton_rect.collidepoint(mouse_pos):
            boton_hover_rect = boton_hover.get_rect(center=boton_rect.center)
            pantalla.blit(boton_hover, boton_hover_rect.topleft)  
        else:
            pantalla.blit(boton_jugar, boton_rect)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.play(-1, start=31.0)
                    en_menu = False

        pygame.display.flip()

# Mostrar el menú antes de iniciar el juego
mostrar_menu()

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if flecha_rect.collidepoint(event.pos):
                mostrar_menu()
                break  # salir del juego y volver al menú

        # Clic en botones (con bloqueo tras primer clic)
        if mostrar_carta and not boton_presionado and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if btn_aceptar_rect.collidepoint(event.pos):
                puntos = min(puntos + 100, 500)

                # Ya no se otorgan bonus por grupo

                mostrar_carta = False
                boton_presionado = True
                if punto_actual and punto_actual not in puntos_usados:
                    puntos_usados.append(punto_actual)
                punto_actual = None

            elif btn_no_rect.collidepoint(event.pos):
                # Penalización fija para todos los grupos
                puntos = max(puntos - 20, 0)
                estabilidad = max(estabilidad - 5, 0)

                # Marcar como muerto el grupo correspondiente
                if "familia" in texto_actual.lower():
                    estado_familias = "muerto"
                if "soldado" in texto_actual.lower():
                    estado_soldados = "muerto"
                if "enfermo" in texto_actual.lower():
                    estado_enfermos = "muerto"
                if "anciano" in texto_actual.lower():
                    estado_ancianos = "muerto"
                if "agricultor" in texto_actual.lower():
                    estado_agricultores = "muerto"

                # Cerrar carta
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

        # Verificar colisión con ratas
        for rata in ratas:
            if not rata.ya_colisiono:
                offset = (moto_rect.x - rata.rect.x, moto_rect.y - rata.rect.y)
                if rata.mask.overlap(moto_mask, offset):
                    rata.ya_colisiono = True
                    estabilidad = max(0, estabilidad - 15)

        # Verificar si la moto está cerca de un punto NO USADO
        for evento in eventos_cartas:
            punto = evento["pos"]
            if punto in puntos_usados:
                continue

            distancia = pygame.Vector2(moto_rect.center).distance_to(punto)
            if distancia < 50:
                texto_actual = evento["mensaje"]
                mostrar_carta = True
                boton_presionado = False
                punto_actual = punto
                break

    # Scroll centrado
    scroll_y = max(0, min(FONDO_ALTO - VENTANA_ALTO, moto_rect.centery - VENTANA_ALTO // 2))

    # Dibujar fondo
    # Scroll centrado en la moto
    scroll_y = max(0, min(FONDO_ALTO - VENTANA_ALTO, moto_rect.centery - VENTANA_ALTO // 2))

    # Dibujar fondo1
    pantalla.blit(fondo, (0, -scroll_y))

    #Personajes
    for obj_img, obj_rect, _ in objetos:
        pantalla.blit(obj_img, (obj_rect.x, obj_rect.y - scroll_y))

    # Dibujar puntos flotantes
    for evento in eventos_cartas:
        punto = evento["pos"]
        if punto in puntos_usados:
            continue  # no mostrar los ya usados
        flotacion = math.sin(tiempo + punto[1] * 0.01) * 5
        x, y = punto
        pygame.draw.circle(pantalla, (255, 255, 255), (x, int(y - scroll_y + flotacion)), 10)

    # Dibujar moto
    pantalla.blit(moto_img, (moto_rect.x, moto_rect.y - scroll_y))


    # Dibujar ratas
    for rata in ratas:
        rata.actualizar(tiempo)
        rata.dibujar(pantalla, scroll_y)


    # Mostrar puntos
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, (255, 255, 255))
    pantalla.blit(texto_puntos, (10, 42))

    # Suponiendo que 'estabilidad' es un número entre 0 y 100
    if estabilidad > 70:
        emoji_actual = emoji_alta
    elif estabilidad > 30:
        emoji_actual = emoji_media
    else:
        emoji_actual = emoji_baja

    # Mostramos el emoji en pantalla
    pantalla.blit(emoji_actual, (VENTANA_ANCHO - 200, 20))  # Ajustá posición
    
    # Mostrar estabilidad
    texto_estabilidad = fuente.render(f"{estabilidad} %", True, (255, 255, 255))
    pantalla.blit(texto_estabilidad, (1160, 35))

    # Derrota inmediata si estabilidad <= 70
    if estabilidad <= 70:
        grupos_estado = {
            "familias": estado_familias,
            "soldados": estado_soldados,
            "agricultores": estado_agricultores,
            "ancianos": estado_ancianos,
            "enfermos": estado_enfermos
        }
        mostrar_resultado(pantalla, puntos, estabilidad, grupos_estado)



    # Mostrar carta si está activa
    if mostrar_carta:
        dibujar_carta()
    else:
        # Verificar final del juego
        if len(puntos_usados) == len(eventos_cartas) and not mostrar_carta:
            grupos_estado = {
                "familias": estado_familias,
                "soldados": estado_soldados,
                "agricultores": estado_agricultores,
                "ancianos": estado_ancianos,
                "enfermos": estado_enfermos
            }

            mostrar_resultado(pantalla, puntos, estabilidad, grupos_estado)
    mouse_pos = pygame.mouse.get_pos()

    if flecha_rect.collidepoint(mouse_pos):
        flecha_zoom = pygame.transform.scale(flecha_img, (48, 48))  # aplica zoom
        pantalla.blit(flecha_zoom, (flecha_rect.x - 4, flecha_rect.y - 4))  # ajusta para que no se desplace raro
    else:
        pantalla.blit(flecha_img, flecha_rect)

    pygame.display.flip()
    tiempo += 0.05
    clock.tick(60)
