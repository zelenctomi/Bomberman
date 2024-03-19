import pygame

class Bomb:
  def __init__(self, x, y, player):
    self.rect = pygame.Rect((x, y, 50, 50))
    self.fuse_time = 150
    self.owner = player
    self.stood_on = True