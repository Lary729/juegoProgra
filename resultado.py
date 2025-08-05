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
    fuente = pygame.font.SysFont("georgia", 28, bold=True)

    # Determinar condiciones
    grupos_vivos = sum(1 for estado in grupos_estado.values() if estado == "vivo")
    soldados_rebeldes = grupos_estado.get("soldados_1") == "muerto" or grupos_estado.get("soldados_2") == "muerto"
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
        pantalla.blit(fondo_ganar if victoria else fondo_perder, (0, 0))

        # Hover en botón
        mouse_pos = pygame.mouse.get_pos()
        if boton_rect.collidepoint(mouse_pos):
            zoom_rect = boton_salir_zoom.get_rect(center=boton_rect.center)
            pantalla.blit(boton_salir_zoom, zoom_rect.topleft)
        else:
            pantalla.blit(boton_salir, boton_rect.topleft)

        # Función para dibujar texto con borde
        def dibujar_texto_bordeado(texto, x, y):
            texto_blanco = fuente.render(texto, True, (255, 255, 255))
            texto_negro = fuente.render(texto, True, (0, 0, 0))
            for dx in [-2, 2]:
                for dy in [-2, 2]:
                    pantalla.blit(texto_negro, (x + dx, y + dy))
            pantalla.blit(texto_blanco, (x, y))

        # Estadísticas generales (columna izquierda)
        y_base_info = 260
        espacio_linea_info = 40
        dibujar_texto_bordeado(f"Puntos: {puntos}", 60, y_base_info)
        dibujar_texto_bordeado(f"Estabilidad: {estabilidad}%", 60, y_base_info + espacio_linea_info)
        dibujar_texto_bordeado(f"Grupos sobrevivientes: {grupos_vivos}", 60, y_base_info + 2 * espacio_linea_info)

        # Mostrar los estados en DOS columnas organizadas
        grupos_col1 = ["familias_1", "soldados_1", "agricultores_1", "ancianos_1", "enfermos_1"]
        grupos_col2 = ["familias_2", "soldados_2", "agricultores_2", "ancianos_2", "enfermos_2"]

        columna_1_x = 500
        columna_2_x = 850
        y_base_grupos = 260
        espacio_linea_grupos = 45

        for i, grupo in enumerate(grupos_col1):
            estado = grupos_estado.get(grupo, "desconocido")
            nombre = grupo.replace("_", " ").capitalize()
            estado_txt = "✅ Vivo" if estado == "vivo" else "☠️ Muerto"
            dibujar_texto_bordeado(f"{nombre}: {estado_txt}", columna_1_x, y_base_grupos + i * espacio_linea_grupos)

        for i, grupo in enumerate(grupos_col2):
            estado = grupos_estado.get(grupo, "desconocido")
            nombre = grupo.replace("_", " ").capitalize()
            estado_txt = "✅ Vivo" if estado == "vivo" else "☠️ Muerto"
            dibujar_texto_bordeado(f"{nombre}: {estado_txt}", columna_2_x, y_base_grupos + i * espacio_linea_grupos)

        pygame.display.flip()
