import pygame
from powerup import Powerup


class Longer_explosion(Powerup):
  def __init__(self, x: int, y: int):
    super().__init__(x, y)
