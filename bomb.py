import pygame
from explosion import Explosion
from settings import Settings


class Bomb:
  def __init__(self, coord: tuple[int, int], size: int, player):
    self.rect: pygame.Rect = pygame.Rect(coord, (size, size))
    self.timer: int = Settings.BOMB_TIMER * Settings.FPS
    self.owner = player
    self.detonator: bool = player.stats['detonator']
    self.id: int = 1
    # Animation #
    self.frame: int = 0
    self.surface: pygame.Surface = self.owner.bomb_frame

  def update(self, value: int = 1) -> int:
    if not self.detonator:
      self.timer -= 1
      self.timer = self.timer * value
    return self.timer

  def explode(self, walls: list[pygame.Rect], crumbly: list[pygame.Rect]) -> list[Explosion]:
    return Explosion((self.rect.x, self.rect.y), walls, crumbly).initiate(self.owner.stats['explosion'])

  def update_frame(self) -> None:
    if not self.detonator:
      if self.frame < 11:
        self.frame += 1

  def update_surface(self, surface: pygame.Surface) -> None:
    if not self.detonator:
      self.surface = surface
