import random
from player import Player
from monster import Monster
from fields import Fields
from settings import Settings


class Spawner:
  def __init__(self, fields: Fields):
    self.players: list[Player] = []
    self.monsters: list[Monster] = []
    self.fields: Fields = fields

  def spawn_players(self, controls: list[dict[str, int]]) -> list[Player]:
    spawn_points: list[tuple[int, int]] = self.__get_player_spawn_points()
    for i in range(len(controls)):
      spawn: tuple[int, int] = spawn_points[i]
      player: Player = Player(spawn, self.fields, controls[i])
      self.players.append(player)
    return self.players
  
  def spawn_monsters(self, count: int) -> list[Monster]:
    '''
    > Spawns monsters at random locations
    
    > The 3 most outer layers of the map are forbidden
    '''
    OFFSET: int = 3 # Forbidden outer layers
    HEIGHT: int = (Settings.HEIGHT // Settings.BLOCK_SIZE) - 1
    WIDTH: int = Settings.WIDTH // Settings.BLOCK_SIZE
    spawn_points: list[tuple[int, int]] = []
    for row in range(HEIGHT - (OFFSET * 2)):
      for col in range(WIDTH - (OFFSET * 2)):
        if self.fields.get_objects(col + OFFSET, row + OFFSET) == []:
          x: int = (col + OFFSET) * Settings.BLOCK_SIZE
          y: int = (row + OFFSET) * Settings.BLOCK_SIZE
          spawn_points.append((x, y))
    for _ in range(count):
      spawn: tuple[int, int] = spawn_points[random.randint(0, len(spawn_points) - 1)]
      monster: Monster = Monster(spawn, self.fields)
      self.monsters.append(monster)
    return self.monsters
  
  def __get_player_spawn_points(self) -> list[tuple[int, int]]:
    '''
    > Returns the 4 corners of the map
    '''
    spawn_points: list[tuple[int, int]] = []
    WIDTH: int = Settings.WIDTH // Settings.BLOCK_SIZE
    HEIGHT: int = (Settings.HEIGHT // Settings.BLOCK_SIZE) - 1
    BLOCK_SIZE: int = Settings.BLOCK_SIZE
    spawn_points.append((BLOCK_SIZE, BLOCK_SIZE))
    spawn_points.append((WIDTH * BLOCK_SIZE - BLOCK_SIZE * 2, HEIGHT * BLOCK_SIZE - BLOCK_SIZE * 2))
    spawn_points.append((BLOCK_SIZE, HEIGHT * BLOCK_SIZE - BLOCK_SIZE * 2))
    spawn_points.append((WIDTH * BLOCK_SIZE - BLOCK_SIZE * 2, BLOCK_SIZE))
    return spawn_points