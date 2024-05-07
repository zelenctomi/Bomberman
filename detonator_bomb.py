import pygame
from explosion import Explosion
from settings import Settings


class Bomb:
  def __init__(self, coord, size: int, player):
    self.rect: pygame.Rect = pygame.Rect(coord, (size, size))
    self.timer: int = Settings.BOMB_TIMER * Settings.FPS
    self.owner = player
    # Animation #
    self.frame: int = 0
    self.surface: pygame.Surface = self.owner.bomb_frame

  def explode(self, walls: list[pygame.Rect]) -> list[Explosion]:
    return Explosion(self.rect.x, self.rect.y, walls).initiate(self.owner.stats['explosion'])
  
  def update_frame(self) -> None:
    if self.frame < 11:
      self.frame += 1

  def update_surface(self, surface: pygame.Surface) -> None:
    self.surface = surface
