import json
import pygame
import random
from enum import Enum
from wall import Wall
from settings import Settings
from crumbly_wall import Crumbly_wall
from barricade_wall import Barricade_wall
from bomb import Bomb, Explosion
from powerups import Powerups, Powerup, Extra_bomb, Longer_explosion, Detonator, Invulnerability, Speed, Barricade, Ghost

GameObject = Wall | Crumbly_wall | Barricade_wall | Bomb | Powerup | Explosion


class Fields:
  def __init__(self):
    self.fields: list[list[list[GameObject]]] = [[[] for _ in range(Settings.WIDTH // Settings.BLOCK_SIZE)]
                                                 for _ in range((Settings.HEIGHT // Settings.BLOCK_SIZE) - 1)]
    self.walls: list[Wall] = []
    self.bombs: list[Bomb] = []
    self.powerups: list[Powerup] = []
    self.explosions: list[Explosion] = []

  def get_walls(self) -> list[Wall]:
    '''
    Returns a list of Walls
    '''
    return [wall for wall in self.walls if not isinstance(wall, Crumbly_wall)]

  def get_crumbly_walls(self) -> list[Wall]:
    return [wall for wall in self.walls if isinstance(wall, Crumbly_wall)]
  
  def get_crumbly_and_barricade_walls(self) -> list[Wall]:
    return [wall for wall in self.walls if isinstance(wall, Crumbly_wall) or isinstance(wall, Barricade_wall)]

  def get(self, x: int, y: int) -> list[GameObject]:
    '''
    Returns a list of GameObjects that can be found on a tile
    '''
    objects: list[GameObject] = []
    target: pygame.Rect = self.snap_to_grid(pygame.Rect(x, y, Settings.BLOCK_SIZE, Settings.BLOCK_SIZE))
    objects.extend(self.fields[target.y // Settings.BLOCK_SIZE][target.x // Settings.BLOCK_SIZE])
    # NOTE: When the object is between two blocks, we need to check both
    if x % Settings.BLOCK_SIZE != 0:
      shift: int = target.x + Settings.BLOCK_SIZE if x % target.x < x else target.x - Settings.BLOCK_SIZE
      objects.extend(self.fields[target.y // Settings.BLOCK_SIZE][shift // Settings.BLOCK_SIZE])
    if y % Settings.BLOCK_SIZE != 0:
      shift: int = target.y + Settings.BLOCK_SIZE if y % target.y < y else target.y - Settings.BLOCK_SIZE
      objects.extend(self.fields[shift // Settings.BLOCK_SIZE][target.x // Settings.BLOCK_SIZE])
    return objects

  def get_surrounding_objects(self, obj: pygame.Rect) -> list[GameObject]:
    '''
    Returns a list of GameObjects that can be found around a tile
    '''
    target: pygame.Rect = self.snap_to_grid(obj)
    potential_collisons: list[GameObject] = []
    for row in range(-1, 2):
      for col in range(-1, 2):
        objects: list[GameObject] = self.get(target.x + row * Settings.BLOCK_SIZE, target.y + col * Settings.BLOCK_SIZE)
        for o in objects:
          if o not in potential_collisons:
            potential_collisons.append(o)
    return potential_collisons

  def set(self, coord: tuple[int, int], obj: GameObject) -> None:
    '''
    Appends objects to the fields matrix and to the lists of Walls, Powerups and Bombs
    '''
    self.fields[coord[1] // Settings.BLOCK_SIZE][coord[0] // Settings.BLOCK_SIZE].append(obj)
    if isinstance(obj, Wall):
      self.walls.append(obj)
    elif isinstance(obj, Powerup):
      self.powerups.append(obj)
    elif isinstance(obj, Bomb):
      self.bombs.append(obj)

  def remove(self, coord: tuple[int, int], obj: GameObject) -> None:
    '''
    Removes specific objects from lists of Walls, Powerups and Bombs
    '''
    self.fields[coord[1] // Settings.BLOCK_SIZE][coord[0] // Settings.BLOCK_SIZE].remove(obj)
    if isinstance(obj, Wall):
      self.walls.remove(obj)
    elif isinstance(obj, Powerup):
      self.powerups.remove(obj)
    elif isinstance(obj, Bomb):
      self.bombs.remove(obj)

  def snap_to_grid(self, rect: pygame.Rect) -> pygame.Rect:
    '''
    Returns a new rectangle that is snapped to the closest grid.
    The alignment bias is towards the right and bottom.
    '''
    return pygame.Rect(rect.centerx // Settings.BLOCK_SIZE * Settings.BLOCK_SIZE,
                       rect.centery // Settings.BLOCK_SIZE * Settings.BLOCK_SIZE,
                       Settings.BLOCK_SIZE, Settings.BLOCK_SIZE)
  
  def field_has_bomb_or_wall(self, x: int, y: int) -> bool:
    return any(isinstance(obj, Bomb) for obj in self.get(x, y)) or any(isinstance(obj, Wall) for obj in self.get(x, y))

  def load_map(self, lvl: int) -> None:
    '''
    Loads a preset map from a .json file. Updates the walls list
    '''
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
    '''
    Calls get_powerup for a random chance to generate a Powerup. If a Powerup is generated, then it is appended to the
    fields matrix and powerups list
    '''
    powerup: (Powerup | None) = Powerups.get_powerup(
      (coord[0] + Settings.POWERUP_OFFSET, coord[1] + Settings.POWERUP_OFFSET), Settings.POWERUP_SIZE)
    if powerup is not None:
      self.set(coord, powerup)

  def update_bombs(self) -> None:
    '''
    Detonates the bomb if the timer runs out.
    '''
    for bomb in self.bombs:
      if bomb.owner.stats['detonator'] == 0:
        if bomb.update() < 0:
          self.explosions.extend(bomb.explode([wall.rect for wall in self.get_walls()],
                                              [wall.rect for wall in self.get_crumbly_and_barricade_walls()]))
          self.remove((bomb.rect.x, bomb.rect.y), bomb)
          bomb.owner.stats['bomb'] += 1
          self.__destroy_crumbly_and_barricade_walls()
  
  def detonate_bombs(self, id) -> None:
    for bomb in self.bombs:
      print(bomb.owner)
    for bomb in self.bombs:
      # if bomb.id == id:
        self.explosions.extend(bomb.explode([wall.rect for wall in self.get_walls()],
                                            [wall.rect for wall in self.get_crumbly_and_barricade_walls()]))
        self.remove((bomb.rect.x, bomb.rect.y), bomb)
        bomb.owner.stats['bomb'] += 1
        self.__destroy_crumbly_and_barricade_walls()

  def update_explosions(self) -> None:
    '''
    Removes Explosions if their lifetime runs out
    '''
    for explosion in self.explosions:
      if explosion.update() == 0:
        self.explosions.remove(explosion)

  def __destroy_crumbly_and_barricade_walls(self) -> None:
    for wall in self.get_crumbly_and_barricade_walls():
      for explosion in self.explosions:
        if pygame.Rect.colliderect(wall.rect, explosion.rect):
          self.remove((wall.rect.x, wall.rect.y), wall)
          coord: tuple[int, int] = (wall.rect.x, wall.rect.y)
          if isinstance(wall, Crumbly_wall):
            self.__drop_powerup(coord)

  def no_bombs_active(self) -> bool:
    '''
    Checks if there are any Bombs or Explosions on the map
    '''
    return len(self.bombs) == 0 and len(self.explosions) == 0
  
  def reload_map(self, lvl: int) -> None:
    '''
    Clears the fields and objects lists then loads a map
    '''
    self.fields = [[[] for _ in range(Settings.WIDTH // Settings.BLOCK_SIZE)]
                   for _ in range((Settings.HEIGHT // Settings.BLOCK_SIZE) - 1)]
    self.walls = []
    self.bombs = []
    self.powerups = []
    self.explosions = []
    self.load_map(lvl)
