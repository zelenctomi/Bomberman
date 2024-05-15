import pygame
import random
from fields import *
from settings import Settings


class Monster:
  DIRECTIONS: list[tuple[int, int, str]] = [(0, -1, 'up'), (0, 1, 'down'), (-1, 0, 'left'), (1, 0, 'right')]
  MAX_SPEED: int = 3

  def __init__(self, coord: tuple[int, int], fields: Fields, rectOffset: int = 0, speed: int = 2) -> None:
    self.hitbox: pygame.Rect = pygame.Rect(coord, (Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    self.rect: pygame.Rect = pygame.Rect(coord, (Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    self.rectOffset: int = rectOffset
    self.rect.y = self.rect.y - rectOffset
    self.fields: Fields = fields
    self.alive: bool = True
    self.speed: int = speed
    self.elapsed: int = 0
    # Animation #
    self.frame: int = 0
    self.direction: str = 'down'
    self.prevDirection: str = 'down'
    # Movement #
    self.x_direction: int
    self.y_direction: int
    self.x_direction, self.y_direction, self.direction = Monster.DIRECTIONS[random.randint(0, 3)]
    self._change_direction()
    # Assets #
    self.surface: pygame.Surface
    self.left: list[pygame.Surface]
    self.right: list[pygame.Surface]
    self.up: list[pygame.Surface]
    self.down: list[pygame.Surface]

  def load_assets(self) -> None:
    '''
    This method loads the monster's assets.
    The hop animation consists of 6 frames for each direction.
    '''
    self.left = [pygame.image.load(f'assets/Monsters/Basic/hop/left/l{i}.png') for i in range(1, 7)]
    self.right = [pygame.image.load(f'assets/Monsters/Basic/hop/right/r{i}.png') for i in range(1, 7)]
    self.up = [pygame.image.load(f'assets/Monsters/Basic/hop/up/u{i}.png') for i in range(1, 7)]
    self.down = [pygame.image.load(f'assets/Monsters/Basic/hop/down/d{i}.png') for i in range(1, 7)]
    # Default Surface #
    self.surface = self.down[0]

  def update_frame(self) -> None:
    '''
    Updates the animation frame based on the movement direction
    '''
    self.__update_surface()
    if self.direction == self.prevDirection and self.frame < len(self.down) - 1:
      self.frame += 1
    else:
      self.frame = 0

  def __update_surface(self) -> None:
    '''
    Updates the texture of the monster based on frame
    '''
    event: str = 'hop'
    direction: str = self.direction
    self.surface = getattr(self, f'{direction}')[self.frame]

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

  def _collides(self, obj: GameObject) -> bool:
    dummy: pygame.Rect = self.hitbox.copy()
    dummy.x += self.x_direction
    dummy.y += self.y_direction
    if pygame.Rect.colliderect(obj.rect, dummy):
      return True
    return False

  def move(self) -> None:
    '''
    Moves the monster. The monster has a chance to randomly change
    direction. If an object is in the way of the monster, then changes
    the direction of it.
    '''
    self.prevDirection = self.direction
    self._randomize_direction()
    potential_collisions: list[GameObject] = self.fields.get_surrounding_objects(self.rect)
    for obj in potential_collisions:
      if self._collides(obj):
        self._change_direction()
        return
    self._update_position(self.x_direction, self.y_direction)

  def __randomize_direction(self) -> None:
    '''
    Rolls a chance to change the direction of the monster, then
    calls a function to randomise the new direction if the roll was
    a success
    '''
    r: int = random.randint(0, 100)
    if r == 50:
      self._change_direction()

  def _update_position(self, x: int, y: int) -> None:
    if self.elapsed - (Monster.MAX_SPEED - self.speed) != 0:
      self.elapsed += 1
      return
    self.rect.x += x
    self.rect.y += y
    self.hitbox.x += x
    self.hitbox.y += y
    self.elapsed = 0

  def respawn(self, coord: tuple[int, int]) -> None:
    '''
    Respawns the monster at given coordinates and restarts the animation
    '''
    self.rect = pygame.Rect(coord, (Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    self.rect.y = self.rect.y - self.rectOffset
    self.hitbox = pygame.Rect(coord, (Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    self.alive = True
    self.frame = 0
