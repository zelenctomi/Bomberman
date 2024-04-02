from fields import *


class Player:
  def __init__(self, spawn: tuple[int, int], fields: Fields, controls: dict[str, pygame.key.key_code]):
    self.rect: pygame.Rect = pygame.Rect(
      spawn, (fields.BLOCK_SIZE, fields.BLOCK_SIZE))
    self.controls: dict[str, pygame.key.key_code] = controls
    self.fields: Fields = fields
    self.bomb: (Bomb | None) = None
    self.is_alive: bool = True
    self.diagonal_move: tuple[int, int] = (1, 0)
    # Stats #
    self.stats: dict[str, int] = {
      'bomb': 1,
      'explosion': 2
    }

  def draw(self, surface: pygame.Surface, dead_surface: pygame.Surface) -> None:
    self.surface: pygame.Surface = surface
    self.dead_surface: pygame.Surface = dead_surface

  def die(self) -> None:
    self.is_alive = False

  def move(self) -> None:
    if self.is_alive:
      key: list[bool] = pygame.key.get_pressed()
      x: int = 0
      y: int = 0
      if key[self.controls['place']]:
        self.__place_bomb()
      if key[self.controls['left']]:
        x = -1
      if key[self.controls['right']]:
        x = 1
      if key[self.controls['up']]:
        y = -1
      if key[self.controls['down']]:
        y = 1
      self.__move_or_collide(x, y)

  def __move_or_collide(self, x: int, y: int) -> None:
    potential_collisions = self.fields.get_objects_around_object(self)
    self.__update_bomb_collision()
    diagonal: bool = True if x != 0 and y != 0 else False
    for obj in potential_collisions:
      x, y = self.__check_collision(x, y, diagonal, obj)
      if x == 0 and y == 0:
        return
    if x != 0 and y != 0: # The player is at an intersection while moving diagonally
      x *= abs(self.diagonal_move[1])
      y *= abs(self.diagonal_move[0])
    self.__update_position(x, y)
  
  def __update_position(self, x: int, y: int) -> None:
    self.rect.x += x
    self.rect.y += y

  def __collides(self, x: int, y: int, obj) -> bool:
    dummy = self.rect.copy()
    dummy.x += x
    dummy.y += y
    if pygame.Rect.colliderect(obj.rect, dummy) and obj != self.bomb:
      return True
    return False
  
  def __check_collision(self, x: int, y: int, diagonal: bool, obj) -> tuple[int, int]: # TODO: Refactor
    collided = False
    if self.__collides(x, 0, obj):
      if not diagonal:
        x, y = self.__slide(x, y)
      else:
        x = 0
      collided = True
    if self.__collides(0, y, obj):
      if not diagonal:
        x, y = self.__slide(x, y)
      else:
        y = 0
      collided = True
    if collided:
      self.__check_powerup(obj) # FIXME: The player picks up the powerup with diagonal movement
      if abs(x + y) == 1:
        self.diagonal_move = (x, y)
    return x, y

  def __slide(self, x: int, y: int) -> tuple[int, int]:
    '''
    SCENARIO:
    The player is moving right, but there is a wall on the right. 
    The player will slide horizontally to the turn thats closer to the player (Same logic for vertical sliding).
    The player will only slide if the player is on 2 blocks at once.
    Returns the direction (x,y) the player will slide.
    '''
    slideX: int = 0
    slideY: int = 0
    current: pygame.Rect = self.fields.snap_to_grid(self.rect)
    target: pygame.Rect = pygame.Rect((current.x // Fields.BLOCK_SIZE + x) * Fields.BLOCK_SIZE,
                                      (current.y // Fields.BLOCK_SIZE + y) * Fields.BLOCK_SIZE + 50,
                                      Fields.BLOCK_SIZE, 
                                      Fields.BLOCK_SIZE)
    # If the target block is not a collision, then the player will slide towards the target block
    potential_collisions = self.fields.get_objects_at_coords(target.x, target.y)
    if potential_collisions == [] or isinstance(potential_collisions[0], Powerup):
      offsetX: int = self.rect.x - current.x
      offsetY: int = self.rect.y - current.y
      slideX = 0 if offsetX == 0 else abs(offsetX) // offsetX * -1
      slideY = 0 if offsetY == 0 else abs(offsetY) // offsetY * -1
    return slideX, slideY

  def __check_powerup(self, obj) -> None:
    if isinstance(obj, Powerup):
      self.__apply_powerup(obj)
      self.fields.get_objects_at_coords(obj.rect.x, obj.rect.y).remove(obj)
      self.fields.powerups.remove(obj)

  def __update_bomb_collision(self) -> None:
    potential_collisions= self.fields.get_objects_at_object(self)
    if self.bomb != None and self.bomb not in potential_collisions:
      self.bomb = None

  def __apply_powerup(self, powerup: Powerup) -> None:
    stat: str
    value: int
    stat, value = powerup.get_bonus()
    self.stats[stat] += value

  def __place_bomb(self) -> None:
    if self.stats['bomb'] > 0 and not self.fields.field_has_bomb(self.rect.x, self.rect.y):
      target: pygame.Rect = self.fields.snap_to_grid(self.rect)
      bomb: Bomb = Bomb((target.x, target.y), Fields.BLOCK_SIZE, self)
      self.fields.set_bomb(target.x, target.y, bomb)
      self.stats['bomb'] -= 1
      self.bomb = bomb
