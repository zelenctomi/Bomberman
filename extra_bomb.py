import pygame
from powerup import powerup

class extra_bomb(powerup):
  def __init__(self, x, y):
    super().__init__(x, y)