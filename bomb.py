import pygame
from explosion import Explosion
from settings import Settings


class Bomb:
  def __init__(self, coord: tuple[int, int], size: int, player):
    self.rect: pygame.Rect = pygame.Rect(coord, (size, size))
    self.timer: int = Settings.BOMB_TIMER * Settings.FPS
    self.owner = player
    # Animation #
    self.frame: int = 0
    self.surface: pygame.Surface = self.owner.bomb_frame

  def update(self, value: int = 1) -> int:
    '''
    Updates bomb timer
    '''
    self.timer -= 1
    self.timer = self.timer * value
    return self.timer

 
  def explode(self, walls: list[pygame.Rect], crumbly: list[pygame.Rect]) -> list[Explosion]:
    '''
    Detonates the bomb, spawning and explosion cascade starting from the bomb's field
    '''
    return Explosion((self.rect.x, self.rect.y), walls, crumbly).initiate(self.owner.stats['explosion'])

  def update_frame(self) -> None:
    '''
    Updates the frame field to a maximum value of 11 (needed for animation)
    '''
    if self.frame < 11:
      self.frame += 1

  def update_surface(self, surface: pygame.Surface) -> None:
    '''
    Updates the bomb texture
    '''
    self.surface = surface
