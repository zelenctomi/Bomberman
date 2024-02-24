import pygame

from powerup import powerup

class longer_explosion(powerup):
  def __init__(self, x, y):
    super().__init__(x, y)