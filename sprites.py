import pygame
from settings import *
from random import randint, choice
from timer import Timer


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z=LAYERS['main']):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.2, -self.rect.height*.75)


class Water(Generic):
    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frame_index = 0

        super().__init__(pos=pos,
                         surface=self.frames[self.frame_index],
                         groups=groups,
                         z=LAYERS['water'])

    def animate(self, dt):
        self.frame_index += 6 * dt

        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)


class WildFlower(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height*0.9)


class Tree(Generic):
    def __init__(self, pos, surface, groups, name):
        super().__init__(pos, surface, groups)

        self.health = 5
        self.alive = True
        self.stump_surface = pygame.image.load(
            f'graphics/stumps/{"small" if name == "Small" else "large"}.png').convert_alpha()
        self.iframe_timer = Timer(200)

        self.apple_surface = pygame.image.load('graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

    def damage(self):
        self.health -= 1

        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            random_apple.kill()

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic((x, y),
                        self.apple_surface,
                        [self.apple_sprites, self.groups()[0]],
                        LAYERS['fruit'])
