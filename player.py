import pygame

class player:
  def __init__(self, x, y, surface):
    self.rect = pygame.Rect((x, y, 25, 25))
    self.bombs_deployed = 0
    self.max_bomb_count = 1
    self.explosion_length = 2
    self.is_alive = True
    self.surface = surface

  def player_died(self):
    self.is_alive = False