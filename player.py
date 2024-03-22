import pygame


class Player:
  def __init__(self, x: int, y: int, surface: pygame.image, dead_surface: pygame.image):
    self.rect: pygame.Rect = pygame.Rect((x, y, 25, 25))
    self.bombs_deployed: int = 0
    self.max_bomb_count: int = 1
    self.explosion_length: int = 2
    self.is_alive: bool = True
    self.surface: pygame.image = surface
    self.dead_surface: pygame.image = dead_surface

  def player_died(self) -> None:
    self.is_alive = False
