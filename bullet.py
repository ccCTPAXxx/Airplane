import pygame
import math
import random


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, shooter, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.shooter = shooter
        if shooter == 'player':
            self.image = pygame.image.load('images/bullet.png')
        else:
            self.image = pygame.image.load('images/emeny_bullet.png')
        self.scale = scale
        self.image = pygame.transform.rotate(self.image, -player.angle)
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (
        int(self.image.get_width() * self.scale),
        int(self.image.get_height() * self.scale)))
        self.rect = self.image.get_rect()

        self.angle = player.angle
        self.speed = 15

        self.rect.x = player.rect.centerx
        self.rect.y = player.rect.centery - 100

    def update(self, HEIGHT, WIDTH, all_sprites, bullets):
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y += self.speed * math.sin(math.radians(self.angle))

        if self.rect.top < 0 or self.rect.bottom > HEIGHT or self.rect.right * 2 < 0 or self.rect.left > WIDTH * 2:
            self.kill()
