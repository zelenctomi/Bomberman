import pygame
from explosion import Explosion
from settings import Settings


class Detonator_bomb:
  def __init__(self, coord, size: int, player):
    self.rect: pygame.Rect = pygame.Rect(coord, (size, size))
    self.detonator: int = 1
    self.owner = player
    # Animation #
    self.frame: int = 0
    self.surface: pygame.Surface = self.owner.bomb_frame

  def explode(self, walls: list[pygame.Rect]) -> list[Explosion]:
    return Explosion(self.rect.x, self.rect.y, walls).initiate(self.owner.stats['explosion'])
  
  def update(self, value: int = 1) -> int:
    self.detonator = 0
    return self.detonator
  
  def update_frame(self) -> None:
    if self.frame < 11:
      self.frame += 1

  def update_surface(self, surface: pygame.Surface) -> None:
    self.surface = surface
