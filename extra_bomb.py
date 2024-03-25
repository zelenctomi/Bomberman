import pygame
from powerup import Powerup


class Extra_bomb(Powerup):
  def __init__(self, x: int, y: int):
    super().__init__(x, y)

  def get_bonus(self) -> tuple[str, int]:
    return "bomb", 1