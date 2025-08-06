import pygame
import sys

VENTANA_ANCHO = 1280
VENTANA_ALTO = 720

def mostrar_resultado(pantalla, puntos, estabilidad, grupos_estado, volver_al_menu):
    fondo_ganar = pygame.image.load("assets/resultado/ganaste.png").convert()
    fondo_ganar = pygame.transform.scale(fondo_ganar, (VENTANA_ANCHO, VENTANA_ALTO))
    fondo_perder = pygame.image.load("assets/resultado/perdiste.png").convert()
    fondo_perder = pygame.transform.scale(fondo_perder, (VENTANA_ANCHO, VENTANA_ALTO))

    fuente = pygame.font.SysFont("georgia", 28, bold=True)

    grupos_vivos = sum(1 for estado in grupos_estado.values() if estado == "vivo")
    soldados_rebeldes = grupos_estado.get("soldados_1") == "muerto" or grupos_estado.get("soldados_2") == "muerto"
    derrota = (grupos_vivos <= 2 or estabilidad <= 70 or soldados_rebeldes)
    victoria = not derrota and estabilidad >= 71

    resultado_activo = True
    while resultado_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    volver_al_menu()
                    return

        pantalla.blit(fondo_ganar if victoria else fondo_perder, (0, 0))

        # 🔳 Caja negra semitransparente centrada
        overlay_rect = pygame.Surface((1160, 420), pygame.SRCALPHA)
        overlay_rect.fill((0, 0, 0, 160))  # Negro con opacidad
        pantalla.blit(overlay_rect, (60, 255))

        # 🖋️ Función de texto con sombra
        def dibujar_texto_bordeado(texto, x, y):
            texto_blanco = fuente.render(texto, True, (255, 255, 255))
            texto_negro = fuente.render(texto, True, (0, 0, 0))
            for dx in [-2, 2]:
                for dy in [-2, 2]:
                    pantalla.blit(texto_negro, (x + dx, y + dy))
            pantalla.blit(texto_blanco, (x, y))

        # ℹ️ Estadísticas generales
        y_base_info = 300
        espacio_linea_info = 40
        dibujar_texto_bordeado(f"Puntos: {puntos}", 90, y_base_info)
        dibujar_texto_bordeado(f"Estabilidad: {estabilidad}%", 90, y_base_info + espacio_linea_info)
        dibujar_texto_bordeado(f"Grupos sobrevivientes: {grupos_vivos}", 90, y_base_info + 2 * espacio_linea_info)

        # 🧍 Estados de grupos
        grupos_col1 = ["familias_1", "soldados_1", "agricultores_1", "ancianos_1", "enfermos_1"]
        grupos_col2 = ["familias_2", "soldados_2", "agricultores_2", "ancianos_2", "enfermos_2"]

        columna_1_x = 510
        columna_2_x = 860
        y_base_grupos = 290
        espacio_linea_grupos = 45

        for i, grupo in enumerate(grupos_col1):
            estado = grupos_estado.get(grupo, "desconocido")
            nombre = grupo.replace("_", " ").capitalize()
            estado_txt = "Vivo" if estado == "vivo" else "Muerto"
            dibujar_texto_bordeado(f"{nombre}: {estado_txt}", columna_1_x, y_base_grupos + i * espacio_linea_grupos)

        for i, grupo in enumerate(grupos_col2):
            estado = grupos_estado.get(grupo, "desconocido")
            nombre = grupo.replace("_", " ").capitalize()
            estado_txt = "Vivo" if estado == "vivo" else "Muerto"
            dibujar_texto_bordeado(f"{nombre}: {estado_txt}", columna_2_x, y_base_grupos + i * espacio_linea_grupos)

        # Instrucción final para salir
        dibujar_texto_bordeado("Presiona ENTER para salir", VENTANA_ANCHO // 2 - 180, 610)

        pygame.display.flip()
