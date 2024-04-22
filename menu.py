import pygame
import json
import sys
from settings import *
from game import *


class Menu():
  # Colors #
  WHITE: tuple[int, int, int] = (255, 255, 255)
  MAP_OUTLINE: tuple[int, int, int] = (222, 172, 245)
  # Map Selection #
  WIDTH: int = Settings.WIDTH // 5
  HEIGHT: int = (Settings.HEIGHT - 50) // 5
  BLOCK_SIZE: int = Settings.BLOCK_SIZE // 5

  def __init__(self):
    pygame.init()
    pygame.display.set_caption('Bomberman')
    pygame.display.set_icon(pygame.image.load('Assets/Bomb/b1.png'))
    self.screen: pygame.Surface = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    self.background: pygame.Surface = pygame.image.load('Assets/Menu/bg.png').convert_alpha()
    self.font_header: pygame.font.Font = pygame.font.Font(Settings.FONT, 50)
    self.font_main: pygame.font.Font = pygame.font.Font(Settings.FONT, 24)
    self.font_main_hover: pygame.font.Font = pygame.font.Font(Settings.FONT, 25)
    self.title_text: pygame.Surface = self.font_header.render('BOMBERMAN', False, Menu.WHITE)
    self.p2_normal_text: pygame.Surface = self.font_main.render('2  PLAYERS', False, Menu.WHITE)
    self.p3_normal_text: pygame.Surface = self.font_main.render('3  PLAYERS', False, Menu.WHITE)
    self.p2_hover_text: pygame.Surface = self.font_main_hover.render('2  PLAYERS', False, Menu.WHITE)
    self.p3_hover_text: pygame.Surface = self.font_main_hover.render('3  PLAYERS', False, Menu.WHITE)
    self.p2_text: pygame.Surface = self.p2_normal_text
    self.p3_text: pygame.Surface = self.p3_normal_text
    self.pointer: pygame.Surface = pygame.image.load('Assets/Menu/pointer.png').convert_alpha()

    # Map Selection #
    self.wall_assets: list[pygame.Surface] = [pygame.transform.scale(pygame.image.load(f'Assets/Walls/Default/wall.png').convert_alpha(), (Menu.BLOCK_SIZE, Menu.BLOCK_SIZE)),
                                              pygame.transform.scale(pygame.image.load(f'Assets/Walls/Default/crumbly.png').convert_alpha(), (Menu.BLOCK_SIZE, Menu.BLOCK_SIZE))]
    self.maps: list[list[list[Wall]]] = []
    self.map_size: tuple[int, int] = (Menu.WIDTH, Menu.HEIGHT)
    self.map_pos: tuple[int, int] = (70, 540)
    self.map_bg: pygame.Surface = pygame.Surface(self.map_size)
    self.map_bg.fill(Settings.BACKGROUND)

    # Text Placement #
    title_size: tuple[int, int] = self.title_text.get_size()
    p2_size: tuple[int, int] = self.p2_text.get_size()
    p3_size: tuple[int, int] = self.p3_text.get_size()
    p2_hover_size: tuple[int, int] = self.p2_hover_text.get_size()
    p3_hover_size: tuple[int, int] = self.p3_hover_text.get_size()
    # NOTE: Not a responsive approach
    self.p2_normal_pos: tuple[int, int] = (Settings.WIDTH // 2 - p2_size[0] // 2, 310)
    self.p3_normal_pos: tuple[int, int] = (Settings.WIDTH // 2 - p3_size[0] // 2, 355)
    self.p2_hover_pos: tuple[int, int] = (Settings.WIDTH // 2 - p2_hover_size[0] // 2, 311)
    self.p3_hover_pos: tuple[int, int] = (Settings.WIDTH // 2 - p3_hover_size[0] // 2, 356)
    self.pointer_p2_pos: tuple[int, int] = (Settings.WIDTH // 2 - p2_size[0] // 2 - 30, 319)
    self.pointer_p3_pos: tuple[int, int] = (Settings.WIDTH // 2 - p3_size[0] // 2 - 30, 364)
    self.title_pos: tuple[int, int] = (Settings.WIDTH // 2 - title_size[0] // 2, 210)
    self.p2_pos: tuple[int, int] = self.p2_normal_pos
    self.p3_pos: tuple[int, int] = self.p3_normal_pos
    self.pointer_pos: tuple[int, int] = self.pointer_p2_pos

    # Game Start #
    self.player_count: int = 2
    self.level: int = 1
    self.__create_maps()

  def __render(self):
    self.__apply_effects()
    self.screen.blit(self.background, (0, 0))
    self.screen.blit(self.title_text, self.title_pos)
    self.screen.blit(self.p2_text, self.p2_pos)
    self.screen.blit(self.p3_text, self.p3_pos)
    self.screen.blit(self.pointer, self.pointer_pos)
    self.__render_maps()

  def __apply_effects(self):
    if self.player_count == 2:
      self.p2_text = self.p2_hover_text
      self.p3_text = self.p3_normal_text
      self.p2_pos = self.p2_hover_pos
      self.p3_pos = self.p3_normal_pos
      self.pointer_pos = self.pointer_p2_pos
    elif self.player_count == 3:
      self.p2_text = self.p2_normal_text
      self.p3_text = self.p3_hover_text
      self.p2_pos = self.p2_normal_pos
      self.p3_pos = self.p3_hover_pos
      self.pointer_pos = self.pointer_p3_pos

  def __create_maps(self):
    WALL: int = 1
    CRUMBLY: int = 2
    with open('map.json', 'r') as file:
      maps: dict = json.load(file)
    for lvl in maps:
      pos: tuple[int, int] = self.map_pos
      map: list[list[Wall]] = []
      for i in range(len(maps[lvl])):
        row: list[Wall] = []
        for num in maps[lvl][i]:
          if num == WALL:
            row.append(Wall(pos, Menu.BLOCK_SIZE))
          elif num == CRUMBLY:
            row.append(Crumbly_wall(pos, Menu.BLOCK_SIZE))
          pos = (pos[0] + Menu.BLOCK_SIZE, pos[1])
        map.append(row)
        pos = (self.map_pos[0], pos[1] + Menu.BLOCK_SIZE)
      self.maps.append(map)
      self.map_pos = (self.map_pos[0] + self.map_size[0] + 75, self.map_pos[1])

  def __render_maps(self):
    THICKNESS: int = 5
    for map in self.maps:
      lvl: int = self.maps.index(map) + 1
      pos: tuple[int, int] = map[0][0].rect.topleft
      outline_size: tuple[int, int] = (self.map_size[0] + THICKNESS * 2, self.map_size[1] + THICKNESS * 2)
      outline_pos: tuple[int, int] = (pos[0] - THICKNESS, pos[1] - THICKNESS)
      outline: pygame.Surface = pygame.Surface(outline_size)
      if lvl != self.level:
        outline.fill(Menu.MAP_OUTLINE)
        outline.set_alpha(25)
      else:
        outline.fill(Menu.WHITE)
      self.screen.blit(outline, outline_pos)
      self.screen.blit(self.map_bg, pos)
      for row in map:
        for wall in row:
          if isinstance(wall, Crumbly_wall):
            self.screen.blit(self.wall_assets[1], wall.rect)
          else:
            self.screen.blit(self.wall_assets[0], wall.rect)

  def __handle_mouse_hover(self, mouse_pos: tuple[int, int]):
    mouse_on_p2: bool = pygame.Rect.collidepoint(pygame.Rect(self.p2_pos, self.p2_text.get_size()), mouse_pos)
    mouse_on_p3: bool = pygame.Rect.collidepoint(pygame.Rect(self.p3_pos, self.p3_text.get_size()), mouse_pos)
    if mouse_on_p2:
      self.player_count = 2
    elif mouse_on_p3:
      self.player_count = 3
    for map in self.maps:
      mouse_on_lvl = pygame.Rect.collidepoint(pygame.Rect(map[0][0].rect.topleft, self.map_size), mouse_pos)
      if mouse_on_lvl:
        self.level = self.maps.index(map) + 1

  def __handle_key_arrow(self, key: int):
    if key == pygame.K_UP:
      self.player_count = 2
    elif key == pygame.K_DOWN:
      self.player_count = 3
    elif key == pygame.K_LEFT:
      if self.level > 1:
        self.level -= 1
    elif key == pygame.K_RIGHT:
      if self.level < len(self.maps):
        self.level += 1

  def __ready(self, event: pygame.event.Event) -> bool:
    '''
    Returns true if the event is a mouse click or enter key press and the menu is ready to start the game
    '''
    return event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)

  def run(self):
    start: bool = False
    while not start:
      self.__render()
      pygame.display.update()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        elif event.type == pygame.MOUSEMOTION:
          self.__handle_mouse_hover(event.pos)
        elif self.__ready(event):
          start = True
        elif event.type == pygame.KEYDOWN:
          self.__handle_key_arrow(event.key)
    pygame.time.wait(100)
    game: Game = Game(self.player_count, self.level)
    game.run()
