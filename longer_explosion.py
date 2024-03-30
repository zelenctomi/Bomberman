from powerup import Powerup


class Longer_explosion(Powerup):
  def __init__(self, coord: tuple[int, int], size: int):
    super().__init__(coord, size)

  def get_bonus(self) -> tuple[str, int]:
    return "explosion", 1
