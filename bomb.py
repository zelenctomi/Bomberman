import pygame


class Bomb:
  def __init__(self, x: int, y: int, player):
    self.rect: pygame.Rect = pygame.Rect((x, y, 50, 50))
    self.fuse_time: int = 150
    self.owner: Player = player
    self.stood_on: bool = True
