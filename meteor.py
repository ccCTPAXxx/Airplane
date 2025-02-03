import pygame
import math
import random
import timeit


class Meteor(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load('images/meteor.png')
        pict_size = random.randrange(40, 60)
        self.image_orig = pygame.transform.scale(self.image_orig,
                                                 (pict_size, pict_size))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)

        pygame.draw.circle(self.image, (255, 255, 255), self.rect.center,
                           self.radius)

        self.rect.x = random.randrange(WIDTH)
        self.side = random.choice([-1, 1])
        if self.side == -1:
            self.rect.y = -self.rect.width
            self.speedy = random.randrange(2, 10)
        else:
            self.rect.y = HEIGHT
            self.speedy = random.randrange(-5, -2)

        self.speedx = random.randrange(-4, 4)

        self.rot = 0
        self.rot_speed = random.randrange(-4, 4)
        self.last_update = pygame.time.get_ticks()
        pict_size = random.randrange(30, 50)
        self.image = pygame.transform.scale(self.image, (pict_size, pict_size))

    def update(self, WIDTH, HEIGHT):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top - 25 > HEIGHT or self.rect.right < -25 or self.rect.left > WIDTH or self.rect.bottom < 0:
            self.rect.x = random.randrange(WIDTH)
            self.side = random.choice([-1, 1])
            if self.side == -1:
                self.rect.y = -self.rect.width
                self.speedy = random.randrange(2, 10)
            else:
                self.rect.y = HEIGHT
                self.speedy = random.randrange(-5, -2)

            self.speedx = random.randrange(-4, 4)

            self.rot_speed = random.randrange(-4, 4)
            self.last_update = pygame.time.get_ticks()

        self.rotate()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 25:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
