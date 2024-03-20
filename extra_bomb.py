import pygame
from powerup import Powerup


class Extra_bomb(Powerup):
  def __init__(self, x, y):
    super().__init__(x, y)
