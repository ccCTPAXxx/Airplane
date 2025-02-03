import pygame
import random
import timeit
import Buster

from player import Player
from emeny import Emeny
from meteor import Meteor

font_name = pygame.font.match_font('arial')


def draw_bar(surf, x, y, pct, color, k):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 20
    fill = (pct / k) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, (0, 0, 0), outline_rect, 2)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


WIDTH = 1480
HEIGHT = 920
FPS = 30
BG_COLOR_MAIN = (50, 50, 80)

start = timeit.default_timer()

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airplane")
clock = pygame.time.Clock()

player_sprite = pygame.sprite.Group()
bullets = pygame.sprite.Group()
emeny_bullets = pygame.sprite.Group()


last_spawn_busters = timeit.default_timer()
next_buster = random.randint(1000, 2500) / 1000
busters = pygame.sprite.Group()


emenies = pygame.sprite.Group()
last_spawn_emeny = timeit.default_timer()
emeny = Emeny(WIDTH, HEIGHT)
emenies.add(emeny)

player = Player(WIDTH, HEIGHT)

mobs = pygame.sprite.Group()

for i in range(8):
    meteor = Meteor(WIDTH, HEIGHT)
    mobs.add(meteor)

player_sprite.add(player)

screen.fill(BG_COLOR_MAIN)
player_sprite.draw(screen)
pygame.display.flip()

resume = False
lives = 100
score = 0

while True:
    clock.tick(FPS)
    screen.fill(BG_COLOR_MAIN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            if event.key == pygame.K_p:
                resume = not resume
                if not start:
                    start = timeit.default_timer()

    if not resume:
        continue

    if timeit.default_timer() - last_spawn_emeny > 1.8:
        emeny = Emeny(WIDTH, HEIGHT)
        emenies.add(emeny)
        last_spawn_emeny = timeit.default_timer()

    if timeit.default_timer() - last_spawn_busters > next_buster:
        buster = random.choice(['heal', 'speed', 'spikes'])
        if buster == 'heal':
            buster = Buster.HealBooster(WIDTH, HEIGHT)
        elif buster == 'speed':
            buster = Buster.SpeedBooster(WIDTH, HEIGHT)
        elif buster == 'spikes':
            buster = Buster.SpikeBooster(WIDTH, HEIGHT)
        elif buster == 'bullet_size':
            buster = Buster.BulletSizeBooster(WIDTH, HEIGHT)
        busters.add(buster)
        last_spawn_busters = timeit.default_timer()
        next_buster = random.randint(1500, 2800) / 1000

    busters.draw(screen)

    player_sprite.update(WIDTH, HEIGHT, player_sprite, bullets)
    player_sprite.draw(screen)

    mobs.update(WIDTH, HEIGHT)
    mobs.draw(screen)

    emenies.update(player, WIDTH, HEIGHT, player_sprite, emeny_bullets)
    emenies.draw(screen)

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Meteor(WIDTH, HEIGHT)
        mobs.add(m)

    hits = pygame.sprite.groupcollide(mobs, emeny_bullets, True, True)
    for hit in hits:
        m = Meteor(WIDTH, HEIGHT)
        mobs.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, True,
                                       pygame.sprite.collide_circle)
    for hit in hits:
        lives -= hit.radius * 2
        mobs.add(Meteor(WIDTH, HEIGHT))
        if lives <= 0:
            quit()

    hits = pygame.sprite.groupcollide(mobs, emenies, True, True)

    for hit in hits:
        e = Emeny(WIDTH, HEIGHT)
        e.kill()
        m = Meteor(WIDTH, HEIGHT)
        mobs.add(m)

    hits = pygame.sprite.spritecollide(player, emenies, True,
                                       pygame.sprite.collide_circle)

    for hit in hits:
        lives -= hit.radius * 2
        if lives <= 0:
            quit()

    hits = pygame.sprite.spritecollide(player, emeny_bullets, True,
                                       pygame.sprite.collide_circle)

    for hit in hits:
        lives -= 20
        if lives <= 0:
            quit()

    pygame.sprite.spritecollide(emeny, emeny_bullets, True,
                                pygame.sprite.collide_circle)

    hits_bust = pygame.sprite.groupcollide(busters, player_sprite, True, False)
    print(hits_bust)
    for hit_bustt in hits_bust:
        if hit_bustt.type == 'heal':
            if lives < 200:
                lives += 20
                lives = min(lives, 200)
        elif hit_bustt.type == 'speed':
            player.speed += 1
        elif hit_bustt.type == 'spike':
            player.spike = True
        elif hit_bustt.type == 'bullet_size':
            if player.bullet_size < 10:
                player.bullet_size += 1
                player.bullet_size = min(player.bullet_size, 10)

    pygame.sprite.groupcollide(emenies, bullets, True, True)

    draw_bar(screen, 5, 5, min(lives, 100), color=(128, 50, 0), k =100)
    draw_bar(screen, 5, 5, max(lives - 100, 0), color=(255, 255, 0), k=100)
    draw_bar(screen, 5, 30, player.ammo, color=(0, 128, 0), k=10)
    draw_bar(screen, 5, 55, player.boost, color=(0, 255, 255), k=50)
    print(timeit.default_timer() - start)

    pygame.display.flip()