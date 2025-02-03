import pygame
import random
import math

from bullet import Bullet


class Emeny(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/emeny.png")
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.choice([WIDTH + 20, -20]), random.randint(0, HEIGHT))
        self.radius = int(self.rect.width * .85 / 2)
        self.angle = 270
        self.angledelta = 5
        self.speed = 4
        self.speedx = 0
        self.speedy = 0
        self.orig_image = self.image
        self.bullet = random.randint(0, 5000)
        self.health = 100

    def count_angle(self, player):
        angle_to_player = math.degrees(
            math.atan2(player.rect.centery - self.rect.centery,
                       player.rect.centerx - self.rect.centerx))

        if angle_to_player > self.angle:
            self.angle += self.angledelta
        elif angle_to_player < self.angle:
            self.angle -= self.angledelta

    def update(self, player, WIDTH, HEIGHT, all_sprites, bullets):
        self.count_angle(player)
        self.speedx = self.speed * math.cos(math.radians(self.angle))
        self.speedy = self.speed * math.sin(math.radians(self.angle))
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rotate()

        angle_to_player = math.degrees(
            math.atan2(player.rect.centery - self.rect.centery,
                       player.rect.centerx - self.rect.centerx))

        if pygame.time.get_ticks() - self.bullet > 1500 and angle_to_player + 15 > self.angle > angle_to_player - 15:
            self.shoot(all_sprites, bullets)
            self.bullet = pygame.time.get_ticks()

    def rotate(self):
        self.image = pygame.transform.rotate(self.orig_image, -self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self, all_sprites, bullets):
        bullet = Bullet(self, 'emeny')
        bullet.rect.centerx = self.rect.centerx  # Пуля будет по центру корабля
        bullet.rect.centery = self.rect.centery  # Пуля будет на уровне
        # центра корабля
        bullet.angle = self.angle  # Передаем угол поворота корабля пуле
        all_sprites.add(bullet)
        bullets.add(bullet)
