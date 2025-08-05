import pygame
import random

class BalaLadron(pygame.sprite.Sprite):
    def __init__(self, x, y, objetivo_rect):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/npcs/ladron/bala.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))  # Asegura visibilidad
        except:
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 0, 0))  # Rojo visible

        self.rect = self.image.get_rect(center=(x, y))

        # Dirección hacia la moto
        origen = pygame.math.Vector2(x, y)
        destino = pygame.math.Vector2(objetivo_rect.center)
        direccion = destino - origen
        if direccion.length() != 0:
            self.velocidad = direccion.normalize() * 7
        else:
            self.velocidad = pygame.math.Vector2(0, 7)

    def update(self):
        self.rect.x += self.velocidad.x
        self.rect.y += self.velocidad.y
        if (self.rect.top > 8000 or self.rect.bottom < 0 or
            self.rect.left < 0 or self.rect.right > 1280):
            self.kill()


class Ladron(pygame.sprite.Sprite):
    def __init__(self, x, y, objetivo=None):
        super().__init__()
        try:
            self.sprites = [
                pygame.image.load("assets/npcs/ladron/1.png").convert_alpha(),
                pygame.image.load("assets/npcs/ladron/2.png").convert_alpha()
            ]
        except:
            self.sprites = [pygame.Surface((60, 80)) for _ in range(2)]
            for sprite in self.sprites:
                sprite.fill((0, 0, 255))  # Azul visible

        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.anim_index = 0
        self.timer_animacion = 0
        self.disparo_cooldown = 620 # Intensidad de disparos
        self.balas = None
        self.get_objetivo = objetivo  # ← función que devuelve el rect
        self.tiempo_persecucion = 120  # 2 segundos a 60fps

    def update(self):
        # Animación
        self.timer_animacion += 1
        if self.timer_animacion >= 12:
            self.anim_index = (self.anim_index + 1) % len(self.sprites)
            self.image = self.sprites[self.anim_index]
            self.timer_animacion = 0

        # Movimiento hacia la moto
        if self.tiempo_persecucion > 0 and self.get_objetivo:
            self.tiempo_persecucion -= 1
            objetivo = self.get_objetivo()
            velocidad = 3
            if self.rect.centerx < objetivo.centerx:
                self.rect.x += velocidad
            elif self.rect.centerx > objetivo.centerx:
                self.rect.x -= velocidad

        # Disparo hacia la moto
        self.disparo_cooldown -= 1
        if self.disparo_cooldown <= 0:
            if self.balas is not None and callable(self.get_objetivo):
                objetivo = self.get_objetivo()
                if objetivo:  # Asegura que no sea None
                    bala = BalaLadron(self.rect.centerx, self.rect.bottom, objetivo)
                    self.balas.add(bala)
            self.disparo_cooldown = 320  # ← Tiempo entre disparos

        # Limitar dentro del ancho
        self.rect.x = max(0, min(self.rect.x, 1280 - self.rect.width))
