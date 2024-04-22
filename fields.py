import json
import pygame
import random
from wall import Wall
from settings import Settings
from crumbly_wall import Crumbly_wall
from bomb import Bomb, Explosion
from powerups import Powerups, Powerup, Extra_bomb, Longer_explosion


class Fields:
  def __init__(self):
    self.fields = [[[] for _ in range(Settings.WIDTH // Settings.BLOCK_SIZE)]
                       for _ in range((Settings.HEIGHT // Settings.BLOCK_SIZE) - 1)]
    self.walls: list[Wall] = []
    self.bombs: list[Bomb] = []
    self.powerups: list[Powerup] = []
    self.explosions: list[Explosion] = []

  def get_crumbly_walls(self) -> list[Crumbly_wall]:
    return [wall for wall in self.walls if isinstance(wall, Crumbly_wall)]

  def get_objects(self, col: int, row: int):
    return self.fields[row][col]

  def get_objects_at_coords(self, x: int, y: int):
    target: pygame.Rect = self.snap_to_grid(pygame.Rect(x, y, Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    return self.get_objects(target.x // Settings.BLOCK_SIZE, target.y // Settings.BLOCK_SIZE)

  def get_objects_at_object(self, obj):
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

  def get_objects_around_object(self, obj):
    potential_collisons: list[pygame.Rect] = []
    for row in range(-1, 2):
      for col in range(-1, 2):
        objects: list[pygame.Rect] = self.get_objects(
          obj.rect.x // Settings.BLOCK_SIZE + row, obj.rect.y // Settings.BLOCK_SIZE + col)
        for o in objects:
          if o not in potential_collisons:
            potential_collisons.append(o)
    return potential_collisons

  def snap_to_grid(self, rect: pygame.Rect) -> pygame.Rect:
    '''
    Returns a mew rectamgle that is snapped to the closest grid.
    '''
    return pygame.Rect(rect.centerx // Settings.BLOCK_SIZE * Settings.BLOCK_SIZE,
                       rect.centery // Settings.BLOCK_SIZE * Settings.BLOCK_SIZE,
                       Settings.BLOCK_SIZE, Settings.BLOCK_SIZE)

  def field_has_bomb(self, x: int, y: int) -> bool:  # TODO: Remove method if not necessary
    return any(isinstance(obj, Bomb) for obj in self.get_objects_at_coords(x, y))

  def load_map(self, lvl: int) -> None:
    WALL: int = 1
    CRUMBLY: int = 2
    with open(f'map.json', 'r') as file:
      maps = json.load(file)
      map = maps[f'lvl{lvl}']
      for y in range(len(map)):
        for x in range(len(map[y])):
          wall: Wall | Crumbly_wall
          coord: tuple[int, int] = (x * Settings.BLOCK_SIZE, y * Settings.BLOCK_SIZE)
          if map[y][x] == WALL:
            wall = Wall(coord, Settings.BLOCK_SIZE)
            self.walls.append(wall)
            self.fields[y][x].append(wall)
          elif map[y][x] == CRUMBLY:
            wall = Crumbly_wall(coord, Settings.BLOCK_SIZE)
            self.walls.append(wall)
            self.fields[y][x].append(wall)

  def __drop_powerup(self, coord: tuple[int, int]) -> None:
    powerup: (Powerup | None) = Powerups.get_powerup(
      (coord[0] + Settings.POWERUP_OFFSET, coord[1] + Settings.POWERUP_OFFSET), Settings.POWERUP_SIZE)
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
