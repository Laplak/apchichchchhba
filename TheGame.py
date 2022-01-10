import pygame
import os
import sys
import random


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(name)

    image = image.convert()
    colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)

    return image


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Cosmo Ball')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()

    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("blue_ufo.png")
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = 5
    sprite.rect.y = 20
    all_sprites.add(sprite)

    running = True
    x_pos = 0
    fps = 30
    v = 20
    clock = pygame.time.Clock()
    while running:
        for i in range(10000):
            screen.fill(pygame.Color('white'),
                        (random.random() * width,
                         random.random() * height, 1, 1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        x_pos += v / fps
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
