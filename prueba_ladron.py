import pygame
import sys
from npc_ladron import Ladron, BalaLadron

pygame.init()
ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
clock = pygame.time.Clock()

# Jugador simulado (la moto)
moto_img = pygame.Surface((60, 80))
moto_img.fill((0, 255, 0))
moto_rect = moto_img.get_rect(center=(ANCHO // 2, ALTO - 100))

# Grupos
ladrones = pygame.sprite.Group()
balas_ladron = pygame.sprite.Group()

# Crear 1 ladrón
ladron = Ladron(ANCHO // 2, 100, objetivo=moto_rect)
ladron.balas = balas_ladron
ladrones.add(ladron)

puntos = 100

# Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento simulado de la moto
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: moto_rect.x -= 5
    if teclas[pygame.K_RIGHT]: moto_rect.x += 5
    if teclas[pygame.K_UP]: moto_rect.y -= 5
    if teclas[pygame.K_DOWN]: moto_rect.y += 5

    pantalla.fill((30, 30, 30))

    # Dibujar moto
    pantalla.blit(moto_img, moto_rect)

    # Actualizar y dibujar ladrones
    ladrones.update()
    for l in ladrones:
        pantalla.blit(l.image, l.rect)

    # Actualizar y dibujar balas
    balas_ladron.update()
    for bala in balas_ladron:
        pantalla.blit(bala.image, bala.rect)

        # Colisión
        if bala.rect.colliderect(moto_rect):
            puntos -= 35
            print("💥 Impacto! Puntos:", puntos)
            bala.kill()

    pygame.display.flip()
    clock.tick(60)
