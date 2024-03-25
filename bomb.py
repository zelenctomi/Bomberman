import pygame
from explosion import Explosion


class Bomb:
  def __init__(self, x: int, y: int, player):
    self.rect: pygame.Rect = pygame.Rect((x, y, 50, 50))
    self.timer: int = 150
    self.owner = player

  def update(self, value: int = 1) -> int:
    self.timer -= 1
    self.timer = self.timer * value
    return self.timer

  def explode(self, walls: list[pygame.Rect]) -> list[Explosion]:
    return Explosion(self.rect.x, self.rect.y, walls).initiate(self.owner.stats['explosion'])