import pygame
import random
from wall import Wall
from crumbly_wall import Crumbly_wall
from bomb import Bomb, Explosion
from powerups import Powerups, Powerup, Extra_bomb, Longer_explosion


class Fields:
  def __init__(self, height: int = 13, width: int = 15):
    self.fields: list[list[list[pygame.Rect]]] = [[[] for _ in range(width)] for _ in range(height)]
    self.walls: list[Wall] = []
    self.bombs: list[Bomb] = []
    self.powerups: list[Powerup] = []
    self.explosions: list[Explosion] = []

  def get_crumbly_walls(self) -> list[Crumbly_wall]:
    return [wall for wall in self.walls if isinstance(wall, Crumbly_wall)]

  def get_objects_at_coords(self, x: int, y: int) -> list[pygame.Rect]:
    return self.fields[y // 50][x // 50]
  
  def get_objects_at_object(self, obj: pygame.Rect) -> list[pygame.Rect]:
    potential_collisons: list[pygame.Rect] = []
    for corner in [obj.rect.topleft, obj.rect.topright, obj.rect.bottomleft, obj.rect.bottomright]:
      for object in self.get_objects_at_coords(corner[0], corner[1]):
        if object not in potential_collisons:
          potential_collisons.append(object)
    return potential_collisons
  
  def field_has_bomb(self, x: int, y: int) -> bool: # TODO: Remove if not necessary
    return any(isinstance(obj, Bomb) for obj in self.get_objects_at_coords(x, y))
  
  def load_walls(self) -> None:
    wall_start_x: int = 0
    for x in range(15):
      wall_start_y: int = 0
      for y in range(13):
        if wall_start_x in [0, 700] or wall_start_y in [0, 600] or \
          (wall_start_x in [100, 200, 300, 400, 500, 600] and wall_start_y in [100, 200, 300, 400, 500]):
          wall: Wall = Wall(wall_start_x, wall_start_y)
          self.walls.append(wall)
          self.fields[y][x].append(wall)
        wall_start_y += 50
      wall_start_x += 50

  def load_crumbly_walls(self) -> None:
    forbidden_spots: list[list[int]] = [[50, 50], [50, 100], [100, 50], [650, 550], [600, 550], [650, 500]]
    crumbly_wall_start_x: int = 50
    for x in range(13):
      crumbly_wall_start_y: int = 50
      for y in range(11):
        if (crumbly_wall_start_x in [100, 200, 300, 400, 500, 600] and crumbly_wall_start_y not in [100, 200, 300, 400, 500]) and \
                [crumbly_wall_start_x, crumbly_wall_start_y] not in forbidden_spots and random.randint(0, 9) > 7:
          crumbly_wall: Crumbly_wall = Crumbly_wall(crumbly_wall_start_x, crumbly_wall_start_y)
          self.walls.append(crumbly_wall)
          self.fields[y + 1][x + 1].append(crumbly_wall)
        crumbly_wall_start_y += 50
      crumbly_wall_start_x += 50

  def drop_powerup(self, x: int, y: int) -> None:
    powerup: (Powerup | None) = Powerups.get_powerup(x, y)
    if powerup is not None:
      self.get_objects_at_coords(x, y).append(powerup)
      self.powerups.append(powerup)

  def set_bomb(self, x: int, y: int, bomb: Bomb) -> None:
    self.bombs.append(bomb)
    self.get_objects_at_coords(x + 10, y + 10).append(bomb)

  def update_bombs(self) -> None:
    for bomb in self.bombs:
      if bomb.update() < 0:
        self.explosions.extend(bomb.explode([wall.rect for wall in self.walls if not isinstance(wall, Crumbly_wall)]))
        self.get_objects_at_coords(bomb.rect.x, bomb.rect.y).remove(bomb)
        self.bombs.remove(bomb)
        bomb.owner.stats['bomb'] += 1
        self.destroy_crumbly_walls()

  def update_explosions(self) -> None:
    for explosion in self.explosions:
      if explosion.update() == 0:
        self.explosions.remove(explosion)

  def destroy_crumbly_walls(self) -> None:
    for wall in self.get_crumbly_walls():
      for explosion in self.explosions:
        if pygame.Rect.colliderect(wall.rect, explosion.rect):
          self.get_objects_at_coords(wall.rect.x, wall.rect.y).remove(wall)
          self.walls.remove(wall)
          self.drop_powerup(wall.rect.x, wall.rect.y)

