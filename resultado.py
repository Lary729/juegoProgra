import pygame
import sys

# =========================
# CONFIGURACIÓN INICIAL
# =========================
VENTANA_ANCHO = 1280
VENTANA_ALTO = 720

# =========================
# FUNCIÓN PRINCIPAL
# =========================
def mostrar_resultado(pantalla, puntos, estabilidad, grupos_estado):
    # Cargar recursos visuales
    fondo_ganar = pygame.image.load("assets/resultado/ganaste.png").convert()
    fondo_perder = pygame.image.load("assets/resultado/perdiste.png").convert()
    boton_salir = pygame.image.load("assets/resultado/boton_salir.png").convert_alpha()
    boton_salir_zoom = pygame.transform.scale_by(boton_salir, 1.2)
    boton_rect = boton_salir.get_rect(center=(VENTANA_ANCHO // 2, VENTANA_ALTO - 60))

    # Fuente para estadísticas
    fuente = pygame.font.SysFont("georgia", 42, bold=True)

    # Determinar condiciones
    grupos_vivos = sum(1 for estado in grupos_estado.values() if estado == "vivo")
    soldados_rebeldes = grupos_estado.get("soldados") == "muerto"
    derrota = (grupos_vivos <= 2 or estabilidad <= 70 or soldados_rebeldes)
    victoria = not derrota and estabilidad >= 71

    # Mostrar resultado
    resultado_activo = True
    while resultado_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        # Fondo según resultado
        if victoria:
            pantalla.blit(fondo_ganar, (0, 0))
        else:
            pantalla.blit(fondo_perder, (0, 0))

        # Efecto hover en botón
        mouse_pos = pygame.mouse.get_pos()
        if boton_rect.collidepoint(mouse_pos):
            zoom_rect = boton_salir_zoom.get_rect(center=boton_rect.center)
            pantalla.blit(boton_salir_zoom, zoom_rect.topleft)
        else:
            pantalla.blit(boton_salir, boton_rect.topleft)

        # Dibujar texto con borde
        def dibujar_texto_bordeado(texto, x, y):
            texto_blanco = fuente.render(texto, True, (255, 255, 255))
            texto_negro = fuente.render(texto, True, (0, 0, 0))
            for dx in [-2, 2]:
                for dy in [-2, 2]:
                    pantalla.blit(texto_negro, (x + dx, y + dy))
            pantalla.blit(texto_blanco, (x, y))

        # Coordenadas para columnas y espaciado
        columna_izquierda_x = 80
        columna_derecha_x = 700
        y_base = 300
        espacio_linea = 60

        # Columna izquierda: estadísticas generales
        dibujar_texto_bordeado(f"Puntos: {puntos}", columna_izquierda_x, y_base)
        dibujar_texto_bordeado(f"Estabilidad: {estabilidad}%", columna_izquierda_x, y_base + espacio_linea)
        dibujar_texto_bordeado(f"Grupos sobrevivientes: {grupos_vivos}", columna_izquierda_x, y_base + 2 * espacio_linea)

        # Columna derecha: estado de cada grupo
        grupos = list(grupos_estado.items())
        for i, (grupo, estado) in enumerate(grupos):
            texto_estado = f"{grupo.capitalize()}: {'✅ Vivo' if estado == 'vivo' else '☠️ Muerto'}"
            y = y_base + i * espacio_linea
            dibujar_texto_bordeado(texto_estado, columna_derecha_x, y)

        pygame.display.flip()