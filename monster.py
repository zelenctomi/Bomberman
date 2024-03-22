import pygame
import random


class Monster:
  def __init__(self, x: int, y: int):
    self.rect: pygame.Rect = pygame.Rect((x, y, 25, 25))
    self.lapse: int = random.randint(400, 1600)
    self.is_alive: bool = True
    self.change_direction_randomly()

  def change_direction_randomly(self) -> None:    # TODO: Rewrite this method to make it more readable
    initial_decision: int = random.randint(0, 3)
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
