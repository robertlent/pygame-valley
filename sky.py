import pygame
from settings import *
from support import import_folder
from sprites import Generic
from random import randint, choice


class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)

    def display(self, dt):
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= 2 * dt

        self.full_surface.fill(self.start_color)
        self.display_surface.blit(self.full_surface,
                                  (0, 0),
                                  special_flags=pygame.BLEND_RGB_MULT)


class Drop(Generic):
    def __init__(self, surface, pos, moving, groups, z):
        super().__init__(pos, surface, groups)
        self.lifetime = randint(350, 500)
        self.start_time = pygame.time.get_ticks()

        self.moving = moving

        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(150, 200)

    def update(self, dt):
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('graphics/rain/drops/')
        self.rain_floor = import_folder('graphics/rain/floor/')
        self.floor_w, self.floor_h = pygame.image.load(
            'graphics/world/ground.png').get_size()

    def create_floor(self):
        Drop(choice(self.rain_floor),
             (randint(0, self.floor_w), randint(0, self.floor_h)),
             False,
             self.all_sprites,
             LAYERS['rain floor'])

    def create_drops(self):
        Drop(choice(self.rain_drops),
             (randint(0, self.floor_w), randint(0, self.floor_h)),
             True,
             self.all_sprites,
             LAYERS['rain drops'])

    def update(self):
        self.create_floor()
        self.create_drops()
