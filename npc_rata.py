import pygame
import random

# Velocidad base (puede ser modificada desde escenario.py si se desea)
VELOCIDAD_RATAS = 8

class Rata:
    def __init__(self, x, y, velocidad=VELOCIDAD_RATAS):
        self.sprites = [
            pygame.image.load("assets/npcs/ratas/1.png").convert_alpha(),
            pygame.image.load("assets/npcs/ratas/2.png").convert_alpha()
        ]
        self.sprite_actual = 0
        self.rect = self.sprites[0].get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.sprites[0])

        self.timer_animacion = 0
        self.ya_colisiono = False

        self.velocidad = velocidad
        self.direccion = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
        self.tiempo_cambio_direccion = random.randint(30, 120)

    def actualizar(self, tiempo):
        # Animación
        self.timer_animacion += tiempo
        if self.timer_animacion > 0.3:
            self.sprite_actual = (self.sprite_actual + 1) % len(self.sprites)
            self.timer_animacion = 0

        # Movimiento más constante
        if self.tiempo_cambio_direccion <= 0:
            self.direccion = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
            self.tiempo_cambio_direccion = random.randint(30, 120)
        else:
            self.tiempo_cambio_direccion -= 1

        # Aplicar movimiento
        self.rect.x += int(self.direccion.x * self.velocidad)
        self.rect.y += int(self.direccion.y * self.velocidad)

        # Limitar para que no se salgan del mapa
        # Limitar horizontalmente a la calle (rebotar si se sale)
        if self.rect.left < 300 or self.rect.right > 980:
            self.direccion.x *= -1  # rebota

        # Mantener límites verticales (como antes)
        self.rect.y = max(0, min(self.rect.y, 8000 - self.rect.height))

    def dibujar(self, pantalla, scroll_y):
        pantalla.blit(self.sprites[self.sprite_actual], (self.rect.x, self.rect.y - scroll_y))
