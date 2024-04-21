import pygame
from powerup import Powerup


class Detonator(Powerup):
  def __init__(self, coord: tuple[int, int], size: int):
    super().__init__(coord, size)

  def get_bonus(self) -> tuple[str, int]:
    return "detonator", 1