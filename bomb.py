import pygame
from explosion import Explosion


class Bomb:
  def __init__(self, coord, size: int, player):
    self.rect: pygame.Rect = pygame.Rect(coord, (size, size))
    self.timer: int = 200
    self.owner = player

  def update(self, value: int = 1) -> int:
    self.timer -= 1
    self.timer = self.timer * value
    return self.timer

  def explode(self, walls: list[pygame.Rect]) -> list[Explosion]:
    return Explosion(self.rect.x, self.rect.y, walls).initiate(self.owner.stats['explosion'])