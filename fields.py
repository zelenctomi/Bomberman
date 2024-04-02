import pygame
import random
from wall import Wall
from crumbly_wall import Crumbly_wall
from bomb import Bomb, Explosion
from powerups import Powerups, Powerup, Extra_bomb, Longer_explosion


class Fields:
  WIDTH: int
  HEIGHT: int
  BLOCK_SIZE: int
  def __init__(self, height: int = 14, width: int = 15, block_size: int = 50):
    Fields.WIDTH = width
    Fields.HEIGHT = height
    Fields.BLOCK_SIZE = block_size
    self.fields = [[[] for _ in range(width)] for _ in range(height)]
    self.walls: list[Wall] = []
    self.bombs: list[Bomb] = []
    self.powerups: list[Powerup] = []
    self.explosions: list[Explosion] = []

  def get_crumbly_walls(self) -> list[Crumbly_wall]:
    return [wall for wall in self.walls if isinstance(wall, Crumbly_wall)]
  
  def get_objects(self, col: int, row: int):
    return self.fields[row][col]

  def get_objects_at_coords(self, x: int, y: int):
    return self.get_objects(x // Fields.BLOCK_SIZE, y // Fields.BLOCK_SIZE)
  
  def get_objects_at_object(self, obj: pygame.Rect):
    potential_collisons = []
    objects = []
    # NOTE rect.bottom and rect.right coordinates always lie one pixel outside of their actual border
    topleft: tuple[int, int] = obj.rect.topleft
    bottomleft: tuple[int, int] = obj.rect.bottomleft
    topright: tuple[int, int] = (obj.rect.topright[0], obj.rect.topright[1] - 1)
    bottomright: tuple[int, int] = (obj.rect.bottomright[0] - 1, obj.rect.bottomright[1] - 1)
    for corner in [topleft, topright, bottomleft, bottomright]:
      objects.extend(self.get_objects_at_coords(corner[0], corner[1]))
    for o in objects:
      if o not in potential_collisons:
        potential_collisons.append(o) 
    return potential_collisons
  
  def get_objects_around_object(self, obj: pygame.Rect) -> list[pygame.Rect]:
    potential_collisons: list[pygame.Rect] = []
    for row in range(-1, 2):
      for col in range(-1, 2):
        objects: list[pygame.Rect] = self.get_objects(obj.rect.x // Fields.BLOCK_SIZE + row, obj.rect.y // Fields.BLOCK_SIZE + col)
        for o in objects:
          if o not in potential_collisons:
            potential_collisons.append(o)
    return potential_collisons
  
  def snap_to_grid(self, rect: pygame.Rect) -> pygame.Rect:
    '''
    Returns a mew rectamgle that is snapped to the closest grid.
    '''
    return pygame.Rect(rect.centerx // Fields.BLOCK_SIZE * Fields.BLOCK_SIZE, 
                       rect.centery // Fields.BLOCK_SIZE * Fields.BLOCK_SIZE, 
                       Fields.BLOCK_SIZE, Fields.BLOCK_SIZE)
  
  def field_has_bomb(self, x: int, y: int) -> bool: # TODO: Remove method if not necessary
    return any(isinstance(obj, Bomb) for obj in self.get_objects_at_coords(x, y))
  
  def load_walls(self) -> None:
    wall_start_x: int = 0
    for x in range(15):
      wall_start_y: int = 50
      for y in range(14):
        if wall_start_x in [0, 700] or wall_start_y in [50, 650] or \
          (wall_start_x in [100, 200, 300, 400, 500, 600] and wall_start_y in [150, 250, 350, 450, 550]):
          wall: Wall = Wall(wall_start_x, wall_start_y)
          self.walls.append(wall)
          self.fields[y][x].append(wall)
        wall_start_y += 50
      wall_start_x += 50

  def load_crumbly_walls(self) -> None:
    forbidden_spots: list[list[int]] = [[50, 100], [50, 150], [100, 100], [650, 600], [600, 600], [650, 550]]#y += 50
    crumbly_wall_start_x: int = 50
    for x in range(13):
      crumbly_wall_start_y: int = 100
      for y in range(11):
        if (crumbly_wall_start_x in [100, 200, 300, 400, 500, 600] and crumbly_wall_start_y not in [150, 250, 350, 450, 550]) and \
                [crumbly_wall_start_x, crumbly_wall_start_y] not in forbidden_spots and random.randint(0, 9) > 7:
          crumbly_wall: Crumbly_wall = Crumbly_wall(crumbly_wall_start_x, crumbly_wall_start_y)
          self.walls.append(crumbly_wall)
          self.fields[y + 1][x + 1].append(crumbly_wall)
        crumbly_wall_start_y += 50
      crumbly_wall_start_x += 50

  def __drop_powerup(self, coord: tuple[int, int]) -> None:
    powerup: (Powerup | None) = Powerups.get_powerup(coord, Fields.BLOCK_SIZE)
    if powerup is not None:
      self.get_objects_at_coords(coord[0], coord[1]).append(powerup)
      self.powerups.append(powerup)

  def set_bomb(self, x: int, y: int, bomb: Bomb) -> None:
    self.bombs.append(bomb)
    self.get_objects_at_coords(x, y).append(bomb)

  def update_bombs(self) -> None:
    for bomb in self.bombs:
      if bomb.update() < 0:
        self.explosions.extend(bomb.explode([wall.rect for wall in self.walls if not isinstance(wall, Crumbly_wall)]))
        self.get_objects_at_coords(bomb.rect.x, bomb.rect.y).remove(bomb)
        self.bombs.remove(bomb)
        bomb.owner.stats['bomb'] += 1
        self.__destroy_crumbly_walls()

  def update_explosions(self) -> None:
    for explosion in self.explosions:
      if explosion.update() == 0:
        self.explosions.remove(explosion)

  def __destroy_crumbly_walls(self) -> None:
    for wall in self.get_crumbly_walls():
      for explosion in self.explosions:
        if pygame.Rect.colliderect(wall.rect, explosion.rect):
          self.get_objects_at_coords(wall.rect.x, wall.rect.y).remove(wall)
          self.walls.remove(wall)
          coord: tuple[int, int] = (wall.rect.x, wall.rect.y)
          self.__drop_powerup(coord)
