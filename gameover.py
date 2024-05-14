import pygame
from settings import Settings


class Gameover:

  def __init__(self, screen: pygame.Surface):
    self.screen = screen
    self.transparency: int = 0
    self.proceed: bool = False
    self.surface: pygame.Surface = pygame.Surface((Settings.WIDTH, Settings.HEIGHT))
    self.surface.fill(Settings.PURPLE)
    self.font: pygame.font.Font = pygame.font.Font(Settings.FONT, 24)
    self.bold_font: pygame.font.Font = pygame.font.Font(Settings.BOLD_FONT, 36)
    self.text: pygame.Surface = self.bold_font.render('GAME OVER', False, Settings.WHITE)
    self.proceed_text: pygame.Surface = self.font.render('Press any key to continue', False, Settings.WHITE)
    self.text.set_alpha(self.transparency)
    self.proceed_text.set_alpha(self.transparency)
    self.proceed_text_fade_in: bool = True
    self.text_pos: tuple[int, int] = (Settings.WIDTH // 2 - self.text.get_width() // 2,
                                      Settings.HEIGHT // 2 - self.text.get_height() // 2 - 300)

  def __fade_in(self):
    '''
    Fades in the gameover screen
    '''
    self.surface.set_alpha(self.transparency)

  def __text_fade_in_down(self):
    '''
    Moves the gameover screen during fade in
    '''
    self.text.set_alpha(self.transparency)
    self.text_pos = (self.text_pos[0], self.text_pos[1] + 3)

  def __proceed_text_flash(self):
    '''
    Implements text fade in
    '''
    transparency: int | None = self.proceed_text.get_alpha()
    transparency = 255 if transparency is None else transparency
    if self.proceed_text_fade_in:
      self.proceed_text.set_alpha(transparency + 3)
      if transparency > 252:
        self.proceed_text_fade_in = False
    else:
      self.proceed_text.set_alpha(transparency - 3)
      if transparency < 1:
        self.proceed_text_fade_in = True

  def render(self):
    '''
    Renders gameover screen
    '''
    if self.transparency < 120:
      self.__fade_in()
    if self.transparency < 253:
      self.__text_fade_in_down()
      self.transparency += 3

    self.surface.fill(Settings.PURPLE)
    self.screen.blit(self.surface, (0, 0))
    self.screen.blit(self.text, self.text_pos)

    if self.transparency > 254:
      self.proceed = True
      self.__proceed_text_flash()
      self.screen.blit(self.proceed_text, (Settings.WIDTH // 2 - self.proceed_text.get_width() // 2,
                                           Settings.HEIGHT // 2 - self.proceed_text.get_height() // 2 + 15))