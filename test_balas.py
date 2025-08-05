import pygame
import sys
from npc_ladron import Ladron, BalaLadron

pygame.init()
ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
clock = pygame.time.Clock()

# Moto falsa
moto = pygame.Rect(ANCHO//2, ALTO - 100, 60, 80)

# Grupos
ladrones = pygame.sprite.Group()
balas = pygame.sprite.Group()

# Crear ladrón con referencia a la moto
ladron = Ladron(ANCHO//2, 100, objetivo=moto)
ladron.balas = balas
ladrones.add(ladron)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pantalla.fill((30, 30, 30))

    # Dibujar moto como rectángulo verde
    pygame.draw.rect(pantalla, (0, 255, 0), moto)

    # Actualizar y dibujar ladrones
    ladrones.update()
    ladrones.draw(pantalla)

    # Actualizar y dibujar balas
    balas.update()
    balas.draw(pantalla)

    pygame.display.flip()
    clock.tick(60)
