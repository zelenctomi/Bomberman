import json
import pygame
import random
from enum import Enum
from wall import Wall
from settings import Settings
from crumbly_wall import Crumbly_wall
from barricade_wall import Barricade_wall
from detonator_bomb import Detonator_bomb
from bomb import Bomb, Explosion
from powerups import Powerups, Powerup, Extra_bomb, Longer_explosion, Detonator, Invulnerability, Speed, Barricade, Ghost

GameObject = Wall | Crumbly_wall | Barricade_wall | Bomb | Detonator_bomb | Powerup | Explosion


class Fields:
  def __init__(self):
    self.fields: list[list[list[GameObject]]] = [[[] for _ in range(Settings.WIDTH // Settings.BLOCK_SIZE)]
                                                 for _ in range((Settings.HEIGHT // Settings.BLOCK_SIZE) - 1)]
    self.walls: list[Wall] = []
    self.bombs: list[Bomb] = []
    self.detonator_bombs: list[Detonator_bomb] = []
    self.powerups: list[Powerup] = []
    self.explosions: list[Explosion] = []

  def get_crumbly_and_barricade_walls(self) -> list[Wall]:
    return [wall for wall in self.walls if isinstance(wall, Crumbly_wall) or isinstance(wall, Barricade_wall)]
  
  def get_crumbly_walls(self) -> list[Wall]:
    return [wall for wall in self.walls if isinstance(wall, Crumbly_wall)]

  def get_crumbly_walls(self) -> list[Crumbly_wall]:
    return [wall for wall in self.walls if isinstance(wall, Crumbly_wall)]

  def get(self, x: int, y: int) -> list[GameObject]:
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
    self.fields[coord[1] // Settings.BLOCK_SIZE][coord[0] // Settings.BLOCK_SIZE].append(obj)
    if isinstance(obj, Wall):
      self.walls.append(obj)
    elif isinstance(obj, Powerup):
      self.powerups.append(obj)
    elif isinstance(obj, Bomb):
      self.bombs.append(obj)

  def remove(self, coord: tuple[int, int], obj: GameObject) -> None:
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
  
  def player_on_wall(self, rect: pygame.Rect) -> bool:
    for wall in self.walls:
      if rect.collidepoint(rect.centerx, rect.centery):
        return True
    return False

  def field_has_bomb_or_wall(self, x: int, y: int) -> bool:
    return any(isinstance(obj, Bomb) for obj in self.get_at_coord(x, y)) or any(isinstance(obj, Detonator_bomb) for obj in self.get_at_coord(x, y)) or any(isinstance(obj, Wall) for obj in self.get_at_coord(x, y))

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
      self.get_at_coord(coord[0], coord[1]).append(powerup)
      self.powerups.append(powerup)

  def set_bomb(self, x: int, y: int, bomb: Bomb) -> None:
    self.bombs.append(bomb)
    self.get_at_coord(x, y).append(bomb)

  def set_detonator_bomb(self, x: int, y: int, detonator_bomb: Detonator_bomb) -> None:
    self.detonator_bombs.append(detonator_bomb)
    self.get_at_coord(x, y).append(detonator_bomb)

  def set_barricade(self, x: int, y: int, barricade: Barricade_wall) -> None:
    self.walls.append(barricade)
    self.get_at_coord(x, y).append(barricade)

  def update_bombs(self) -> None:
    for bomb in self.bombs:
      if bomb.owner.stats['detonator'] == 0:
        if bomb.update() < 0:
          self.explosions.extend(bomb.explode([wall.rect for wall in self.walls if not isinstance(wall, Crumbly_wall) and not isinstance(wall, Barricade_wall)]))
          self.get_at_coord(bomb.rect.x, bomb.rect.y).remove(bomb)
          self.bombs.remove(bomb)
          self.__destroy_crumbly_and_barricade_walls()

  def detonator_explosion(self, detonator_bomb: Detonator_bomb):
    for bomb in self.detonator_bombs:
      if bomb.owner == detonator_bomb.owner:
        self.explosions.extend(bomb.explode([wall.rect for wall in self.walls if not isinstance(wall, Crumbly_wall) and not isinstance(wall, Barricade_wall)]))
        self.get_at_coord(bomb.rect.x, bomb.rect.y).remove(bomb)
        self.detonator_bombs.remove(bomb)
        self.__destroy_crumbly_and_barricade_walls()


  def update_explosions(self) -> None:
    for explosion in self.explosions:
      if explosion.update() == 0:
        self.explosions.remove(explosion)

  def __destroy_crumbly_walls(self) -> None:
    for wall in self.get_crumbly_walls():
      for explosion in self.explosions:
        if pygame.Rect.colliderect(wall.rect, explosion.rect):
          self.remove((wall.rect.x, wall.rect.y), wall)
          self.__drop_powerup((wall.rect.x, wall.rect.y))

  def no_bombs_active(self) -> bool:
    return len(self.bombs) == 0 and len(self.explosions) == 0
  
  def reload_map(self, lvl: int) -> None:
    self.fields = [[[] for _ in range(Settings.WIDTH // Settings.BLOCK_SIZE)]
                   for _ in range((Settings.HEIGHT // Settings.BLOCK_SIZE) - 1)]
    self.walls = []
    self.bombs = []
    self.powerups = []
    self.explosions = []
    self.load_map(lvl)
