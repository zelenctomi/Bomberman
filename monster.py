import pygame, random
from fields import Fields
from settings import Settings


class Monster:
  DIRECTIONS: list[tuple[int, int]] = [(0, -1), (0, 1), (-1, 0), (1, 0)]

  def __init__(self, spawn: tuple[int, int], fields: Fields):
    self.rect: pygame.Rect = pygame.Rect(spawn, (Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    self.fields: Fields = fields
    self.x_direction: int
    self.y_direction: int
    self.x_direction, self.y_direction = Monster.DIRECTIONS[random.randint(0, 3)]
    self.is_alive: bool = True
    self.__change_direction()

  def die(self) -> None:
    self.is_alive = False

  def __change_direction(self) -> None:
    directions: list[tuple[int, int]] = Monster.DIRECTIONS.copy()
    directions.remove((self.x_direction, self.y_direction))
    self.x_direction, self.y_direction = directions[random.randint(0, 2)]

  def __turn_on_collision(self, obj) -> bool:
    dummy = self.rect.copy()
    dummy.x += self.x_direction
    dummy.y += self.y_direction
    if pygame.Rect.colliderect(obj.rect, dummy):
      self.__change_direction()
      return True
    return False
  
  def move(self) -> None:
    self.__randomize_direction()
    potential_collisions = self.fields.get_objects_around_object(self)
    for obj in potential_collisions:
      if self.__turn_on_collision(obj):
        return
    self.__update_position(self.x_direction, self.y_direction)

  def __randomize_direction(self) -> None:
    rotate = random.randint(0, 100)
    if rotate == 50:
      self.__change_direction()

  def __update_position(self, x: int, y: int) -> None:
    self.rect.x += x
    self.rect.y += y