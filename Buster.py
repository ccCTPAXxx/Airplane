import random

import pygame


class Booster(pygame.sprite.Sprite):
    def __init__(self, image, screen_width, screen_height, type):
        super().__init__()
        self.image = pygame.image.load(image)
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)


class HealBooster(Booster):
    def __init__(self, screen_width, screen_height):
        super().__init__('images/heal_booster.png', screen_width, screen_height, 'heal')

class SpeedBooster(Booster):
    def __init__(self, screen_width, screen_height):
        super().__init__('images/speed_booster.png', screen_width, screen_height, 'speed')

class SpikeBooster(Booster):
    def __init__(self, screen_width, screen_height):
        super().__init__('images/spike_booster.png', screen_width, screen_height, 'spike')

class BulletSizeBooster(Booster):
    def __init__(self, screen_width, screen_height):
        super().__init__('images/spike_booster.png', screen_width, screen_height, 'bullet')