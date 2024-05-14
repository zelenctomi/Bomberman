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
    self.hopLeft = [pygame.image.load(f'assets/Monsters/Basic/hop/left/l{i}.png') for i in range(1, 7)]
    self.hopRight = [pygame.image.load(f'assets/Monsters/Basic/hop/right/r{i}.png') for i in range(1, 7)]
    self.hopUp = [pygame.image.load(f'assets/Monsters/Basic/hop/up/u{i}.png') for i in range(1, 7)]
    self.hopDown = [pygame.image.load(f'assets/Monsters/Basic/hop/down/d{i}.png') for i in range(1, 7)]
    # Default Surface #
    self.surface = self.hopDown[0]

  def update_frame(self) -> None:
    '''
    Updates the animation frame based on the movement direction
    '''
    self.__update_surface()
    if self.direction == self.prevDirection and self.frame < 5:
      self.frame += 1
    else:
      self.frame = 0

  def __update_surface(self) -> None:
    '''
    Updates the texture of the monster based on frame
    '''
    event: str = 'hop'
    direction: str = self.direction
    self.surface = getattr(self, f'{event}{direction.capitalize()}')[self.frame]

  def die(self) -> None:
    '''
    Kills the monster
    '''
    self.is_alive = False

  def __change_direction(self) -> None:
    '''
    Changes the direction of the monster randomly
    '''
    directions: list[tuple[int, int, str]] = Monster.DIRECTIONS.copy()
    directions.remove((self.x_direction, self.y_direction, self.direction))
    self.x_direction, self.y_direction, self.direction = directions[random.randint(0, 2)]

  def __turn_on_collision(self, obj: GameObject) -> bool:
    '''
    Changes the direction of the monster if it hits a wall
    '''
    dummy: pygame.Rect = self.rect.copy()
    dummy.x += self.x_direction
    dummy.y += self.y_direction
    if pygame.Rect.colliderect(obj.rect, dummy):
      self.__change_direction()
      return True
    return False

  def move(self) -> None:
    '''
    Moves the monster. The monster has a chance to randomly change
    direction. If an object is in the way of the monster, then changes
    the direction of it.
    '''
    self.prevDirection = self.direction
    self.__randomize_direction()
    potential_collisions: list[GameObject] = self.fields.get_surrounding_objects(self.rect)
    for obj in potential_collisions:
      if self.__turn_on_collision(obj):
        return
    self.__update_position(self.x_direction, self.y_direction)

  def __randomize_direction(self) -> None:
    '''
    Rolls a chance to change the direction of the monster, then
    calls a function to randomise the new direction if the roll was
    a success
    '''
    r: int = random.randint(0, 100)
    if r == 50:
      self.__change_direction()

  def __update_position(self, x: int, y: int) -> None:
    '''
    Updates the coordinates of the monster
    '''
    self.rect.x += x
    self.rect.y += y

  def respawn(self, coord: tuple[int, int]) -> None:
    '''
    Respawns the monster at given coordinates and restarts the animation
    '''
    self.rect = pygame.Rect(coord, (Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    self.alive = True
    self.frame = 0
    self.surface = self.hopDown[0]
