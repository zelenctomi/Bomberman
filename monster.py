import pygame
import random
from fields import *
from settings import Settings


class Monster:
  DIRECTIONS: list[tuple[int, int, str]] = [(0, -1, 'up'), (0, 1, 'down'), (-1, 0, 'left'), (1, 0, 'right')]

  def __init__(self, coord: tuple[int, int], fields: Fields):
    self.rect: pygame.Rect = pygame.Rect(coord, (Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    self.fields: Fields = fields
    self.is_alive: bool = True
    # Animation #
    self.frame: int = 0
    self.direction: str = 'down'
    self.prevDirection: str = 'down'
    # Movement #
    self.x_direction: int
    self.y_direction: int
    self.x_direction, self.y_direction, self.direction = Monster.DIRECTIONS[random.randint(0, 3)]
    self.__change_direction()
    # Assets #
    self.surface: pygame.Surface
    self.hopLeft: list[pygame.Surface]
    self.hopRight: list[pygame.Surface]
    self.hopUp: list[pygame.Surface]
    self.hopDown: list[pygame.Surface]

  def load_assets(self) -> None:
    '''
    This method loads the monster's assets.
    The hop animation consists of 6 frames for each direction.
    '''
    self.hopLeft = [pygame.image.load(f'assets/Monster/hop/left/l{i}.png') for i in range(1, 7)]
    self.hopRight = [pygame.image.load(f'assets/Monster/hop/right/r{i}.png') for i in range(1, 7)]
    self.hopUp = [pygame.image.load(f'assets/Monster/hop/up/u{i}.png') for i in range(1, 7)]
    self.hopDown = [pygame.image.load(f'assets/Monster/hop/down/d{i}.png') for i in range(1, 7)]
    # Default Surface #
    self.surface = self.hopDown[0]

  def update_frame(self) -> None:
    self.__update_surface()
    if self.direction == self.prevDirection and self.frame < 5:
      self.frame += 1
    else:
      self.frame = 0

  def __update_surface(self) -> None:
    event: str = 'hop'
    direction: str = self.direction
    self.surface = getattr(self, f'{event}{direction.capitalize()}')[self.frame]

  def die(self) -> None:
    self.is_alive = False

  def __change_direction(self) -> None:
    directions: list[tuple[int, int, str]] = Monster.DIRECTIONS.copy()
    directions.remove((self.x_direction, self.y_direction, self.direction))
    self.x_direction, self.y_direction, self.direction = directions[random.randint(0, 2)]

  def __turn_on_collision(self, obj: GameObject) -> bool:
    dummy: pygame.Rect = self.rect.copy()
    dummy.x += self.x_direction
    dummy.y += self.y_direction
    if pygame.Rect.colliderect(obj.rect, dummy):
      self.__change_direction()
      return True
    return False

  def move(self) -> None:
    self.prevDirection = self.direction
    self.__randomize_direction()
    potential_collisions: list[GameObject] = self.fields.get_surrounding_objects(self.rect)
    for obj in potential_collisions:
      if self.__turn_on_collision(obj):
        return
    self.__update_position(self.x_direction, self.y_direction)

  def __randomize_direction(self) -> None:
    r: int = random.randint(0, 100)
    if r == 50:
      self.__change_direction()

  def __update_position(self, x: int, y: int) -> None:
    self.rect.x += x
    self.rect.y += y
