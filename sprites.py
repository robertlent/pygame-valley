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


class Particle(Generic):
    def __init__(self, pos, surface, groups, z, duration=200):
        super().__init__(pos, surface, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        mask_surface = pygame.mask.from_surface(self.image)
        new_surface = mask_surface.to_surface()
        new_surface.set_colorkey((0, 0, 0))
        self.image = new_surface

    def update(self, dt):
        current_time = pygame.time.get_ticks()

        if current_time - self.start_time > self.duration:
            self.kill()


class Tree(Generic):
    def __init__(self, pos, surface, groups, name, add_inventory):
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

        self.add_inventory = add_inventory

    def damage(self):
        self.health -= 1

        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(random_apple.rect.topleft,
                     random_apple.image,
                     self.groups()[0],
                     LAYERS['fruit'])
            self.add_inventory('apple')
            random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            Particle(self.rect.topleft,
                     self.image,
                     self.groups()[0],
                     LAYERS['fruit'],
                     350)
            self.add_inventory('wood')
            self.image = self.stump_surface
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height*0.6)
            self.alive = False

    def update(self, dt):
        if self.alive:
            self.check_death()

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic((x, y),
                        self.apple_surface,
                        [self.apple_sprites, self.groups()[0]],
                        LAYERS['fruit'])
