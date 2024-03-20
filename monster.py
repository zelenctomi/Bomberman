import pygame
import random


class Monster:
  def __init__(self, x, y):
    self.rect = pygame.Rect((x, y, 25, 25))
    self.lapse = random.randint(400, 1600)
    self.change_direction_randomly()
    self.is_alive = True

  def change_direction_randomly(self):
    initial_decision = random.randint(0, 3)
    if initial_decision == 0:
      self.x_direction = 0
      self.y_direction = -1
    elif initial_decision == 1:
      self.x_direction = 0
      self.y_direction = 1
    elif initial_decision == 2:
      self.x_direction = -1
      self.y_direction = 0
    else:
      self.x_direction = 1
      self.y_direction = 0
