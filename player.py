import pygame
import math
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/player.png")


        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)

        # pygame.draw.circle(self.image, (255, 255, 255), self.rect.center,
        #                    self.radius)

        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.angle = 270
        self.angledelta = 5
        self.speed = 6.5
        self.speedx = 0
        self.speedy = 0
        self.orig_image = self.image
        self.ammo = 10
        self.last_update_ammo = pygame.time.get_ticks()

        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

        self.boost = 50
        self.last_boost = pygame.time.get_ticks()
        self.spike = False

    def kill_by_wall(self, WIDTH, HEIGHT):
        if self.rect.right > WIDTH + 8:
            quit()
        if self.rect.left < -8:
            quit()
        if self.rect.top < -8:
            quit()
        if self.rect.bottom > HEIGHT + 8:
            quit()

    def update(self, WIDTH, HEIGHT, all_sprites, bullets):
        curr_speed = self.speed
        if self.speed >= 10:
            self.speed = 10

        if self.spike:
            for i in range(3):
                self.spike_shoot(all_sprites, bullets, 360)
            self.spike = False

        if pygame.time.get_ticks() - self.last_update_ammo > 3000 and self.ammo < 10:
            self.last_update_ammo = pygame.time.get_ticks()
            self.ammo += 1

        keystate = pygame.key.get_pressed()

        if keystate[
            pygame.K_SPACE]:
            self.shoot(all_sprites, bullets)

        if keystate[pygame.K_UP]:
            if pygame.time.get_ticks() - self.last_boost > 20:
                self.last_boost = pygame.time.get_ticks()
                self.boost -= 1

            if self.boost > 0:
                curr_speed += 6

        if self.boost < 50:
            if pygame.time.get_ticks() - self.last_boost >= 500:
                self.last_boost = pygame.time.get_ticks()
                self.boost += 2

        if keystate[pygame.K_LEFT]:
            self.angle -= self.angledelta

        if keystate[pygame.K_RIGHT]:
            self.angle += self.angledelta

        self.speedx = math.cos(math.radians(self.angle)) * curr_speed
        self.speedy = math.sin(math.radians(self.angle)) * curr_speed

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.kill_by_wall(WIDTH, HEIGHT)
        self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotate(self.orig_image, -self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self, all_sprites, bullets):
        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()

            if self.ammo <= 0:
                return
            bullet = Bullet(self, 'player')
            bullet.rect.centerx = self.rect.centerx  # Пуля будет по центру корабля
            bullet.rect.centery = self.rect.centery  # Пуля будет на уровне центра корабля
            bullet.angle = self.angle  # Передаем угол поворота корабля пуле
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.ammo -= 1

    def spike_shoot(self, all_sprites, bullets, number):
        for i in range(0, 360, 360 // number):
            bullet = Bullet(self, 'player', 0.5)
            bullet.rect.centerx = self.rect.centerx  # Пуля будет по центру корабля
            bullet.rect.centery = self.rect.centery  # Пуля будет на уровне центра корабля
            bullet.angle = i  # Передаем угол поворота корабля пуле
            all_sprites.add(bullet)
            bullets.add(bullet)