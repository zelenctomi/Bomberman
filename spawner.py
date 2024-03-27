import random
from player import Player
from monster import Monster
from fields import Fields


class Spawner:
  def __init__(self, fields: Fields):
    self.players: list[Player] = []
    self.monsters: list[Monster] = []
    self.fields: Fields = fields

  def spawn_players(self, spawn_points: list[tuple[int, int]], controls: list[dict[str, int]]) -> list[Player]:
    for i in range(len(spawn_points)):
      coord: tuple[int, int] = spawn_points[i]
      player: Player = Player(coord[0], coord[1], self.fields, controls[i])
      self.players.append(player)
    return self.players

  def spawn_monsters(self, count: int) -> list[Monster]: # TODO: Rewrite this method
    forbidden_spots: list[list[int]] = [[50, 50], [50, 100], [100, 50], [650, 550], [600, 550], [650, 500]]
    for _ in range(count):
      can_spawn: bool = False
      while not can_spawn:
        spawn_x: int = random.randint(1, 13) * 50
        spawn_y: int = random.randint(1, 11) * 50
        spawn_x += random.randint(0, 24)
        spawn_y += random.randint(0, 24)
        if [spawn_x, spawn_y] in forbidden_spots:
          continue
        can_spawn = True
        for wall in self.fields.walls:
          if wall.rect.collidepoint(spawn_x, spawn_y):
            can_spawn = False
      self.monsters.append(Monster(spawn_x, spawn_y, self.fields))
    return self.monsters