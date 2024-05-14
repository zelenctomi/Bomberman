import pygame
from settings import Settings


class Scoreboard:

  def __init__(self):
    pygame.init()
    self.rect_bg1: pygame.Rect = pygame.Rect(Settings.SCOREBOARD_RECT_1, (800, 66))
    self.rect_bg2: pygame.Rect = pygame.Rect(Settings.SCOREBOARD_RECT_1, (800, 66))
    self.rect_bg2.right = 0
    self.__load_asset()
    self.__write_datas()

  def __load_asset(self):
    self.scoreboard_surface: pygame.Surface = pygame.image.load(
        'Assets/Menu/Status_Bar.png').convert_alpha()
    
  def slide(self):
    self.rect_bg1.x += 1
    self.rect_bg2.x += 1
    if self.rect_bg1.left == Settings.WIDTH:
      self.rect_bg1.right = 0
    elif self.rect_bg2.left == Settings.WIDTH:
      self.rect_bg2.right = 0

  def __write_datas(self):
    font = pygame.font.Font(None, 20)

    player_1 = font.render('Player 1', True, (255, 255, 255))
    player_2 = font.render('Player 2', True, (255, 255, 255))
    player_3 = font.render('Player 3', True, (255, 255, 255))

    player_1_rect = player_1.get_rect()
    player_2_rect = player_2.get_rect()
    player_3_rect = player_3.get_rect()

    player_1_rect.midleft = (10, 640)
    player_2_rect.midleft = (100, 640)
    player_3_rect.midleft = (190, 640)
