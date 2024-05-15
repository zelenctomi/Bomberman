import pygame


class Powerup:
  def __init__(self, coord: tuple[int, int], size: int):
    self.rect: pygame.Rect = pygame.Rect(coord, (size, size))

  def get_bonus(self) -> tuple[str, int]:
    '''
    Applies the Powerup bonus (abstract)
    '''
    ...
