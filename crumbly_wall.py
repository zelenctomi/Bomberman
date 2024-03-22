import pygame


class Crumbly_wall:
  def __init__(self, x: int, y: int):
    self.rect: pygame.Rect = pygame.Rect((x, y, 50, 50))
    self.destroyed: bool = False
