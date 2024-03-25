import pygame


class Powerup:
  def __init__(self, x: int, y: int):
    self.rect: pygame.Rect = pygame.Rect((x, y, 50, 50))

  def get_bonus(self) -> tuple[str, int]:
    ...
