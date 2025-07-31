import pygame
import sys

# Inicializar Pygame y mixer
pygame.init()
pygame.mixer.init()

# Ventana
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Héroes del Hambre")

# Fuente
font = pygame.font.SysFont('georgia', 24)
font_titulo = pygame.font.SysFont('georgia', 32, bold=True)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Música
pygame.mixer.music.load("assets/musica_menu.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Imágenes
background_menu = pygame.image.load("assets/portada.png").convert()
background_juego = pygame.image.load("assets/presentacion1.png").convert()
background_juego = pygame.transform.scale(background_juego, (WIDTH, HEIGHT))

boton_jugar_original = pygame.image.load("assets/boton_jugar.png").convert_alpha()
boton_jugar_img = pygame.transform.smoothscale(boton_jugar_original, (200, 80))
boton_jugar_hover = pygame.transform.smoothscale(boton_jugar_original, (int(235 * 1.1), int(80 * 1.1)))

boton_confirmar_original = pygame.image.load("assets/boton_confirmar.png").convert_alpha()
boton_confirmar_img = pygame.transform.smoothscale(boton_confirmar_original, (200, 80))
boton_confirmar_hover = pygame.transform.smoothscale(boton_confirmar_original, (int(200 * 1.1), int(80 * 1.1)))

flecha_original = pygame.image.load("assets/flecha_atras.png").convert_alpha()
flecha_img = pygame.transform.smoothscale(flecha_original, (60, 60))
flecha_hover = pygame.transform.smoothscale(flecha_original, (int(60 * 1.1), int(60 * 1.1)))

# Posiciones de botones
boton_x, boton_y = 20, 615
confirmar_x, confirmar_y = 1020, 630
flecha_x, flecha_y = 10, 10

# Rects
confirmar_rect = pygame.Rect(confirmar_x, confirmar_y, 200, 80)
flecha_rect = pygame.Rect(flecha_x, flecha_y, 60, 60)

# Variables de juego
estado_juego = "menu"
comida_disponible = 100
ronda = 1

# Lista de grupos
grupos = [
    {"nombre": "Familias con niños", "salud": 100, "minimo": 25, "asignado": 0},
    {"nombre": "Ancianos", "salud": 100, "minimo": 20, "asignado": 0},
    {"nombre": "Enfermos", "salud": 100, "minimo": 15, "asignado": 0},
    {"nombre": "Trabajadores", "salud": 100, "minimo": 30, "asignado": 0},
]

# Consecuencias
mostrando_consecuencias = False
mensajes_consecuencias = []

# Función: dibujar texto centrado
def texto_centrado(texto, y, fuente, color=(245,245,230)):
    sombra = fuente.render(texto, True, (30,30,30))
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    sombra_rect = rect.copy()
    sombra_rect.x += 3  # sombra solo hacia la derecha
    sombra_rect.y += 2  # y un poco hacia abajo
    screen.blit(sombra, sombra_rect)
    screen.blit(render, rect)

# Bucle principal
running = True
while running:
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if mostrando_consecuencias and (
            event.type == pygame.MOUSEBUTTONDOWN or
            (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
        ):
            mostrando_consecuencias = False
            comida_disponible = 100
            ronda += 1
            mensajes_consecuencias = []

        elif estado_juego == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(boton_x, boton_y, 235, 98).collidepoint(event.pos):
                estado_juego = "juego"

        elif estado_juego == "juego" and not mostrando_consecuencias:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if confirmar_rect.collidepoint((mx, my)):
                    mensajes_consecuencias = []
                    for grupo in grupos:
                        if grupo["asignado"] >= grupo["minimo"]:
                            mensajes_consecuencias.append(f"{grupo['nombre']}: Estables")
                        elif grupo["asignado"] > 0:
                            grupo["salud"] -= 20
                            mensajes_consecuencias.append(f"{grupo['nombre']}: Recibieron poco (-20 salud)")
                        else:
                            grupo["salud"] -= 40
                            mensajes_consecuencias.append(f"{grupo['nombre']}: No recibieron nada (-40 salud)")
                        grupo["asignado"] = 0

                    mostrando_consecuencias = True

                if flecha_rect.collidepoint((mx, my)):
                    estado_juego = "menu"

    # Dibujar pantallas
    if estado_juego == "menu":
        screen.blit(background_menu, (0, 0))
        boton_rect = pygame.Rect(boton_x, boton_y, 235, 98)
        if boton_rect.collidepoint(mouse_pos):
            offset_x = (int(235 * 1.1) - 235) // 2
            offset_y = (int(98 * 1.1) - 98) // 2
            screen.blit(boton_jugar_hover, (boton_x - offset_x, boton_y - offset_y))
        else:
            screen.blit(boton_jugar_img, (boton_x, boton_y))

    elif estado_juego == "juego":
        screen.blit(background_juego, (0, 0))
        texto_centrado(f"Ronda {ronda} - Comida disponible: {comida_disponible}", 30, font_titulo)
        
        if confirmar_rect.collidepoint(mouse_pos):
            screen.blit(boton_confirmar_hover, (confirmar_x - 10, confirmar_y - 5))
        else:
            screen.blit(boton_confirmar_img, (confirmar_x, confirmar_y))

        if flecha_rect.collidepoint(mouse_pos):
            screen.blit(flecha_hover, (flecha_x - 5, flecha_y - 5))
        else:
            screen.blit(flecha_img, (flecha_x, flecha_y))

        if mostrando_consecuencias:
            overlay = pygame.Surface((WIDTH - 200, HEIGHT - 200), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (100, 100))

            texto_centrado("RESULTADO DE LA RONDA", 140, font_titulo)

            for i, mensaje in enumerate(mensajes_consecuencias):
                texto_centrado(mensaje, 200 + i * 40, font)

            texto_centrado("Presiona Enter o haz clic para continuar", 550, font)

    pygame.display.flip()

pygame.quit()
sys.exit()
