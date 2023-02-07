import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *
from random import choice


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']


class SoilLayer:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()

        self.soil_surfaces = import_folder_dict('graphics/soil')
        self.water_surfaces = import_folder('graphics/soil_water/')

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        ground = pygame.image.load('graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]

        for x, y, _ in load_pygame('graphics/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []

        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, pos):
        for rect in self.hit_rects:
            if rect.collidepoint(pos):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')
                pos = soil_sprite.rect.topleft
                surface = choice(self.water_surfaces)

                WaterTile(pos, surface, [self.all_sprites, self.water_sprites])

    def remove_water(self):
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def create_soil_tiles(self):
        self.soil_sprites.empty()

        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    t = 'X' in self.grid[index_row - 1][index_col]
                    b = 'X' in self.grid[index_row + 1][index_col]
                    r = 'X' in row[index_col + 1]
                    l = 'X' in row[index_col - 1]

                    tile_type = 'o'

                    # soil patches on all sides
                    if all((t, b, r, l)):
                        tile_type = 'x'

                    # soil patch on the left side
                    if l and not any((t, r, b)):
                        tile_type = 'r'

                    # soil patch on the right side
                    if r and not any((t, l, b)):
                        tile_type = 'l'

                    # soil patches on the both sides
                    if r and l and not any((t, b)):
                        tile_type = 'lr'

                    # soil patch above
                    if t and not any((b, l, r)):
                        tile_type = 'b'

                    # soil patch below
                    if b and not any((t, l, r)):
                        tile_type = 't'

                    # soil patch above and below
                    if t and b and not any((l, r)):
                        tile_type = 'tb'

                    # soil patch below and left side
                    if b and l and not any((t, r)):
                        tile_type = 'tr'

                    # soil patch obove and left side
                    if t and l and not any((b, r)):
                        tile_type = 'br'

                    # soil patch below and right side
                    if b and r and not any((t, l)):
                        tile_type = 'tl'

                    # soil patch above and right side
                    if t and r and not any((b, l)):
                        tile_type = 'bl'

                    # soil patch top, bottom, and right
                    if all((t, b, r)) and not l:
                        tile_type = 'tbr'

                    # soil patch top, bottom, and left
                    if all((t, b, l)) and not r:
                        tile_type = 'tbl'

                    # soil patch top, right, and left
                    if all((t, r, l)) and not b:
                        tile_type = 'lrb'

                    # soil patch bottom, right, and left
                    if all((b, r, l)) and not t:
                        tile_type = 'lrt'

                    SoilTile((index_col * TILE_SIZE, index_row * TILE_SIZE),
                             self.soil_surfaces[tile_type],
                             [self.all_sprites, self.soil_sprites])
