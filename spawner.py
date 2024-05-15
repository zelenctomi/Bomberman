import random
from player import Player
from monster import Monster
from drone import Drone
from fields import Fields
from settings import Settings


class Spawner:
  def __init__(self, fields: Fields):
    self.players: list[Player] = []
    self.monsters: list[Monster] = []
    self.fields: Fields = fields
    self.player_spawns: list[tuple[int, int]] = self.__get_player_spawn_points()

  def spawn_players(self, count: int) -> list[Player]:
    '''
    Fills the player list with players that have set spawn locations and movement keys
    '''
    for i in range(count):
      spawn: tuple[int, int] = self.player_spawns[i]
      player: Player = Player(spawn, self.fields, Settings.CONTROLS[i])
      self.players.append(player)
    return self.players

  def spawn_monsters(self, count: int) -> list[Monster]:
    '''
    Fills the monster list with monsters that have random spawn locations
    '''
    spawn_points: list[tuple[int, int]] = self.__get_monster_spawn_points()
    for _ in range(count):
      spawn: tuple[int, int] = spawn_points[random.randint(0, len(spawn_points) - 1)]
      monster: Monster = self.__get_random_monster(spawn)
      self.monsters.append(monster)
    # The Drone should have the biggest z-index, so it should be at the end of the list
    self.monsters.sort(key=lambda monster: isinstance(monster, Drone))
    return self.monsters
  
  def __get_random_monster(self, spawn: tuple[int, int]) -> Monster:
    return random.choice([Monster(spawn, self.fields), Drone(spawn, self.fields)])

  def __get_player_spawn_points(self) -> list[tuple[int, int]]:
    '''
    Returns the 4 corners of the map.
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
  
  def __get_monster_spawn_points(self) -> list[tuple[int, int]]:
    '''
    Returns a list of spawn points for monsters.

    The 3 most outer layers of the map are forbidden.
    '''
    OFFSET: int = 3  # Forbidden outer layers
    HEIGHT: int = (Settings.HEIGHT // Settings.BLOCK_SIZE) - 1
    WIDTH: int = Settings.WIDTH // Settings.BLOCK_SIZE
    spawn_points: list[tuple[int, int]] = []
    for row in range(HEIGHT - (OFFSET * 2)):
      for col in range(WIDTH - (OFFSET * 2)):
        if self.fields.get((col + OFFSET) * Settings.BLOCK_SIZE, (row + OFFSET) * Settings.BLOCK_SIZE) == []:
          x: int = (col + OFFSET) * Settings.BLOCK_SIZE
          y: int = (row + OFFSET) * Settings.BLOCK_SIZE
          spawn_points.append((x, y))
    return spawn_points
  
  def respawn_players(self, players: list[Player]) -> None:
    '''
    Respawns all players to their default spawnpoints
    '''
    for i in range(len(players)):
      players[i].respawn(self.player_spawns[i])

  def respawn_monsters(self, monsters: list[Monster]) -> None:
    '''
    Respawns all monsters to random spawnpoints
    '''
    spawn_points: list[tuple[int, int]] = self.__get_monster_spawn_points()
    for i in range(len(monsters)):
      monsters[i].respawn(spawn_points[i])
