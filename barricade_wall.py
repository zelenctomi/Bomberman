from wall import Wall


class Barricade_wall(Wall):
  def __init__(self, coord: tuple[int, int], size: int):
    super().__init__(coord, size)
