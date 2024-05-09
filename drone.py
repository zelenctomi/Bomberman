from monster import *


class Drone(Monster):
  def __init__(self, coord: tuple[int, int], fields: Fields) -> None:
    super().__init__(coord, fields, rectOffset=15, speed=1)
    self.target: pygame.Rect | None = None
    self.load_assets()

  def load_assets(self) -> None:
    '''
    This method loads the assets for the drone.
    The fly animation consists of 4 frames for each direction.
    '''
    self.left = [pygame.image.load(f'assets/Monsters/Drone/fly/left/l{i}.png') for i in range(1, 5)]
    self.right = [pygame.image.load(f'assets/Monsters/Drone/fly/right/r{i}.png') for i in range(1, 5)]
    self.up = [pygame.image.load(f'assets/Monsters/Drone/fly/up/u{i}.png') for i in range(1, 5)]
    self.down = [pygame.image.load(f'assets/Monsters/Drone/fly/down/d{i}.png') for i in range(1, 5)]
    # Default Surface #
    self.surface = self.down[0]

  def move(self) -> None:
    self.prevDirection = self.direction
    # self._randomize_direction()
    potential_collisions: list[GameObject] = self.fields.get_surrounding_objects(self.hitbox)
    for obj in potential_collisions:
      if self._collides(obj) and not self.__can_fly_over():
        self._change_direction()
        return
      elif self.target:
        self.__can_fly_over()
    self._update_position(self.x_direction, self.y_direction)

  def __can_fly_over(self) -> bool:
    empty_tile_ahead: bool = False
    if self.target and self.target.x == self.hitbox.x and self.target.y == self.hitbox.y:
      self.target = None
      print('target reached')
    elif self.target:
      return True

    snapped: pygame.Rect = self.fields.snap_to_grid(self.hitbox)
    if snapped.x == self.hitbox.x and snapped.y == self.hitbox.y:
      col, row = self.hitbox.x // Settings.BLOCK_SIZE, self.hitbox.y // Settings.BLOCK_SIZE
      tiles_ahead: int
      if self.direction == 'left':
        tiles_ahead = col
      elif self.direction == 'right':
        tiles_ahead = Settings.COLS - col
      elif self.direction == 'up':
        tiles_ahead = row
      else:
        tiles_ahead = Settings.ROWS - row

      for i in range(1, tiles_ahead):
        x, y = (col + (i * self.x_direction)) * Settings.BLOCK_SIZE, (row + (i * self.y_direction)) * Settings.BLOCK_SIZE
        tile: list[GameObject] = self.fields.get(x, y)
        if len(tile) == 0:
          empty_tile_ahead = True
          self.target = pygame.Rect(x, y, Settings.BLOCK_SIZE, Settings.BLOCK_SIZE)
          print(f'{self.hitbox.x} {self.hitbox.y} -> target set: {self.target.x} {self.target.y}')
          break
    return empty_tile_ahead

  def respawn(self, coord: tuple[int, int]) -> None:
    self.rect = pygame.Rect(coord, (Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    self.rect.y = self.rect.y - self.rectOffset
    self.hitbox = pygame.Rect(coord, (Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    self.target = None
    self.alive = True
    self.frame = 0