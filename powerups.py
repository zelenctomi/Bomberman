import random
from powerup import Powerup
from extra_bomb import Extra_bomb
from longer_explosion import Longer_explosion
from detonator import Detonator


class Powerups:
    
  @staticmethod
  def get_powerup(coord: tuple[int, int], size: int) -> (Powerup | None):
    POWERUPS: list[Powerup] = [Extra_bomb(coord, size), Longer_explosion(coord, size), Detonator(coord, size)]
    PROBABILITY: int = 5
    r: int = random.randint(0, PROBABILITY * len(POWERUPS) - PROBABILITY)
    if r > len(POWERUPS) - 1:
      return
    else:
      return POWERUPS[r]
