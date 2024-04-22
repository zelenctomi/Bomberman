import pygame


class Wall:
  def __init__(self, coord: tuple[int, int], size: int):
    self.rect: pygame.Rect = pygame.Rect(coord, (size, size))
