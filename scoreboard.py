import pygame
from settings import Settings


class Scoreboard:

  def __init__(self, screen: pygame.Surface, player_count: int):
    self.screen = screen
    self.player_count: int = player_count
    self.scores: list[int] = [0 for _ in range(player_count)]
    self.font: pygame.font.Font = pygame.font.Font(Settings.FONT, 24)
    self.pos: pygame.Rect = pygame.Rect((0, Settings.HEIGHT - Settings.SCOREBOARD_HEIGHT),
                                        (Settings.WIDTH, Settings.SCOREBOARD_HEIGHT))
    self.surface: pygame.Surface
    self.heads: list[pygame.Surface] = []
    self.points: list[pygame.Surface] = self.__create_points()
    self.rects: tuple[pygame.Rect, pygame.Rect] = self.__create_rects()
    self.containers: list[tuple[pygame.Surface, pygame.Rect]] = self.__create_containers()
    self.__load_assets()

  def __load_assets(self):
    self.surface: pygame.Surface = pygame.image.load('Assets/Scoreboard/bar.png').convert_alpha()
    colors: list[tuple[int, int, int]] = [Settings.P2_COLOR, Settings.P3_COLOR]
    for i in range(self.player_count):
      surface: pygame.Surface = pygame.image.load('Assets/Scoreboard/head.png').convert_alpha()
      colors_index: int = i - 1
      if i > 0:
        surface.fill(colors[colors_index], special_flags=pygame.BLEND_SUB)
      self.heads.append(surface)

  def __create_rects(self) -> tuple[pygame.Rect, pygame.Rect]:
    size: tuple[int, int] = (Settings.BLOCK_SIZE, Settings.BLOCK_SIZE)
    heads: pygame.Rect = pygame.Rect((0, 0), size)
    points: pygame.Rect = pygame.Rect((Settings.BLOCK_SIZE, 0), size)
    return (heads, points)

  def __create_points(self) -> list[pygame.Surface]:
    points: list[pygame.Surface] = []
    for i in range(self.player_count):
      points.append(self.font.render(f'{self.scores[i]}', False, Settings.WHITE))
    return points

  def __create_containers(self) -> list[tuple[pygame.Surface, pygame.Rect]]:
    ITEMS: int = 3
    centerY: int = Settings.SCOREBOARD_HEIGHT - Settings.BLOCK_SIZE
    size: tuple[int, int] = (Settings.BLOCK_SIZE * ITEMS, Settings.BLOCK_SIZE)
    containers: list[tuple[pygame.Surface, pygame.Rect]] = [(pygame.Surface(size).convert_alpha(), pygame.Rect((Settings.BLOCK_SIZE, centerY), size)),
                                                            (pygame.Surface(size).convert_alpha(), pygame.Rect((Settings.WIDTH - (size[0] + Settings.BLOCK_SIZE), centerY), size))]
    if self.player_count == 3:  # Position the 3rd rect in the middle
      containers.append((pygame.Surface(size).convert_alpha(), pygame.Rect((300, centerY), size)))
    for container in containers:
      container[0].fill(Settings.PURPLE)  # Transparent
      pass
    return containers

  def render(self):
    for i in range(self.player_count):
      text_size: tuple[int, int] = self.points[i].get_size()
      point_pos: tuple[int, int] = (self.rects[1].centerx - text_size[0] // 2, self.rects[1].centery - text_size[1] // 2)

      self.containers[i][0].blit(self.heads[i], self.rects[0])
      self.containers[i][0].blit(self.points[i], point_pos)
      self.surface.blit(self.containers[i][0], self.containers[i][1])
    self.screen.blit(self.surface, self.pos)

  def update(self, player: int):
    self.scores[player] += 1
    self.points[player] = self.font.render(f'{self.scores[player]}', False, Settings.WHITE)
    self.containers[player][0].fill(Settings.PURPLE) # Clear the container

  # def slide(self):
  #   self.rect_bg1.x += 1
  #   self.rect_bg2.x += 1
  #   if self.rect_bg1.left == Settings.WIDTH:
  #     self.rect_bg1.right = 0
  #   elif self.rect_bg2.left == Settings.WIDTH:
  #     self.rect_bg2.right = 0
