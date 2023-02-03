import pygame
from settings import *


def draw_hitboxes(self, player, offset_rect):
    pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
    hitbox_rect = player.hitbox.copy()
    hitbox_rect.center = offset_rect.center
    pygame.draw.rect(self.display_surface,
                     'green',
                     hitbox_rect,
                     5)
    target_pos = (offset_rect.center +
                  PLAYER_TOOL_OFFSET[player.status.split('_')[0]])
    pygame.draw.circle(self.display_surface,
                       'blue',
                       target_pos,
                       5)
