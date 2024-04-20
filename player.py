from fields import *


class Player:
  DIRECTIONS: dict[tuple[int, int], str] = {(0, -1): 'up', (0, 1): 'down', (-1, 0): 'left', (1, 0): 'right'}
  def __init__(self, spawn: tuple[int, int], fields: Fields, controls: dict[str, int]):
    self.rect: pygame.Rect = pygame.Rect(
      spawn, (fields.BLOCK_SIZE, fields.BLOCK_SIZE))
    self.controls: dict[str, int] = controls
    self.fields: Fields = fields
    self.bomb: (Bomb | None) = None
    self.is_alive: bool = True
    self.diagonal_move: tuple[int, int] = (1, 0)
    # Stats #
    self.stats: dict[str, int] = {
      'bomb': 1,
      'explosion': 2
    }
    # Animation #
    self.frame: int = 0
    self.idle: bool = True
    self.direction: str = 'down'
    self.prevDirection: str = 'down'
    # Assets #
    self.surface: pygame.Surface
    self.idleLeft: list[pygame.Surface]
    self.idleRight: list[pygame.Surface]
    self.idleUp: list[pygame.Surface]
    self.idleDown: list[pygame.Surface]
    self.walkLeft: list[pygame.Surface]
    self.walkRight: list[pygame.Surface]
    self.walkUp: list[pygame.Surface]
    self.walkDown: list[pygame.Surface]

  def load_assets(self, playerNum: int) -> None:
    '''
    This method loads the player's assets.
    The idle animation consists of 8 frames for each direction, with the first 4 frames and the last 4 frames being the same.
    The walk animation consists of 8 frames for each direction.
    '''
    # Idle Frames #
    self.idleLeft = [pygame.image.load(f'Assets/Players/p{playerNum}/idle/left/l1.png').convert_alpha() for _ in range(1, 5)]
    self.idleRight = [pygame.image.load(f'Assets/Players/p{playerNum}/idle/right/r1.png').convert_alpha() for _ in range(1, 5)]
    self.idleUp = [pygame.image.load(f'Assets/Players/p{playerNum}/idle/up/u1.png').convert_alpha() for _ in range(1, 5)]
    self.idleDown = [pygame.image.load(f'Assets/Players/p{playerNum}/idle/down/d1.png').convert_alpha() for _ in range(1, 5)]
    self.idleLeft.extend([pygame.image.load(f'Assets/Players/p{playerNum}/idle/left/l2.png').convert_alpha() for _ in range(1, 5)])
    self.idleRight.extend([pygame.image.load(f'Assets/Players/p{playerNum}/idle/right/r2.png').convert_alpha() for _ in range(1, 5)])
    self.idleUp.extend([pygame.image.load(f'Assets/Players/p{playerNum}/idle/up/u2.png').convert_alpha() for _ in range(1, 5)])
    self.idleDown.extend([pygame.image.load(f'Assets/Players/p{playerNum}/idle/down/d2.png').convert_alpha() for _ in range(1, 5)])
    # Walk Frames #
    self.walkLeft = [pygame.image.load(f'Assets/Players/p{playerNum}/walk/left/l{i}.png').convert_alpha() for i in range(1, 9)]
    self.walkRight = [pygame.image.load(f'Assets/Players/p{playerNum}/walk/right/r{i}.png').convert_alpha() for i in range(1, 9)]
    self.walkUp = [pygame.image.load(f'Assets/Players/p{playerNum}/walk/up/u{i}.png').convert_alpha() for i in range(1, 9)]
    self.walkDown = [pygame.image.load(f'Assets/Players/p{playerNum}/walk/down/d{i}.png').convert_alpha() for i in range(1, 9)]
    # Default Surface #
    self.surface = self.idleDown[0]

  def die(self) -> None:
    self.is_alive = False

  def update_frame(self) -> None:
    if self.direction == self.prevDirection and self.frame < 7:
      self.frame += 1
    else:
      self.frame = 0
    self.__update_surface()

  def __update_surface(self) -> None:
    event: str = 'walk' if not self.idle else 'idle'
    direction: str = self.direction
    self.surface = getattr(self, f'{event}{direction.capitalize()}')[self.frame]
    
  def move(self) -> None:
    if self.is_alive:
      key: tuple[bool, ...] = pygame.key.get_pressed()
      x: int = 0
      y: int = 0
      if key[self.controls['place']]:
        self.__place_bomb()
      if key[self.controls['left']]:
        x += -1
      if key[self.controls['right']]:
        x += 1
      if key[self.controls['up']]:
        y += -1
      if key[self.controls['down']]:
        y += 1

      x, y = self.__move_or_collide(x, y)

      if x != 0 or y != 0:
        self.prevDirection = self.direction
        self.direction = Player.DIRECTIONS[(x, y)]
        self.idle = False
      else:
        self.idle = True

      # self.__update_frame()
      # self.__update_surface()

  def __move_or_collide(self, x: int, y: int) -> tuple[int, int]:
    potential_collisions = self.fields.get_objects_around_object(self)
    self.__update_bomb_collision()
    for obj in potential_collisions:
      x, y = self.__check_collision(x, y, obj)
      if x == 0 and y == 0:
        return x, y
    if x != 0 and y != 0: # The player is at an intersection while moving diagonally
      x *= abs(self.diagonal_move[1])
      y *= abs(self.diagonal_move[0])
    self.__update_position(x, y)
    return x, y
  
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
  
  def __check_collision(self, x: int, y: int, obj) -> tuple[int, int]: # TODO: Refactor
    collided = False
    diagonal: bool = True if x != 0 and y != 0 else False
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
                                      (current.y // Fields.BLOCK_SIZE + y) * Fields.BLOCK_SIZE,
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
