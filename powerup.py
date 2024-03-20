import pygame


class Powerup:
  def __init__(self, x, y):
    self.rect = pygame.Rect((x, y, 50, 50))
