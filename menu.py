import pygame
from settings import *
from timer import Timer


class Menu:
    def __init__(self, player, toggle_menu):
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/ComicNeue-Bold.ttf', 25)

        self.width = 400
        self.space = 10
        self.padding = 8

        self.options = list(self.player.item_inventory.keys()) + \
            list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

        self.index = 0
        self.timer = Timer(200)

    def display_money(self):
        text_surface = self.font.render(f'${self.player.money}',
                                        False,
                                        'Black')
        text_rect = text_surface.get_rect(
            midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface,
                         'White',
                         text_rect.inflate(10, 10),
                         0,
                         6)
        self.display_surface.blit(text_surface, text_rect)

    def setup(self):
        self.text_surfaces = []
        self.total_height = 0

        for index, item in enumerate(self.options):
            if index <= self.sell_border:
                text_surface = self.font.render(
                    f'{item} (${SALE_PRICES[item]})',
                    False,
                    'Black')
            else:
                text_surface = self.font.render(
                    f'{item} seeds (${PURCHASE_PRICES[item]})',
                    False,
                    'Black')

            self.text_surfaces.append(text_surface)
            self.total_height += text_surface.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfaces) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2,
                                     self.menu_top,
                                     self.width,
                                     self.total_height)

        self.buy_text = self.font.render('Buy', False, 'Red')
        self.sell_text = self.font.render('Sell', False, 'Green')

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                current_item = self.options[self.index]

                if self.index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]
                else:
                    seed_price = PURCHASE_PRICES[current_item]

                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= seed_price

        if self.index < 0:
            self.index = len(self.options) - 1

        if self.index > len(self.options) - 1:
            self.index = 0

    def show_entry(self, text_surface, amount, top, selected):
        background_rect = pygame.Rect(self.main_rect.left,
                                      top,
                                      self.width,
                                      text_surface.get_height() + self.padding * 2)
        pygame.draw.rect(self.display_surface,
                         'White',
                         background_rect,
                         0,
                         6)

        text_rect = text_surface.get_rect(
            midleft=(self.main_rect.left + 20, background_rect.centery))
        self.display_surface.blit(text_surface, text_rect)

        amount_surface = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surface.get_rect(
            midright=(self.main_rect.right - 20, background_rect.centery))
        self.display_surface.blit(amount_surface, amount_rect)

        if selected:
            pygame.draw.rect(self.display_surface,
                             'Black',
                             background_rect,
                             4,
                             6)

            if self.index <= self.sell_border:
                pos_rect = self.sell_text.get_rect(
                    midleft=(self.main_rect.left + 250, background_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else:
                pos_rect = self.buy_text.get_rect(
                    midleft=(self.main_rect.left + 250, background_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()
        self.display_money()

        for text_index, text_surface in enumerate(self.text_surfaces):
            top = self.main_rect.top + text_index * \
                (text_surface.get_height() + (self.padding * 2) + self.space)

            amount_list = list(self.player.item_inventory.values()) +\
                list(self.player.seed_inventory.values())
            amount = amount_list[text_index]

            self.show_entry(text_surface,
                            amount,
                            top,
                            self.index == text_index)
