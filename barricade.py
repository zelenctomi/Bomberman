from powerup import Powerup


class Barricade(Powerup):

  def __init__(self, coord: tuple[int, int], size: int):
    super().__init__(coord, size)

  def get_bonus(self) -> tuple[str, int]:
    '''
    Serves to apply the bonus upon pickup
    '''
    return "barricade", 3
