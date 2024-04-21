import pygame
import sys
from pygame.locals import * # type: ignore
from settings import *
from game import *

class Start_menu():

    def __init__(self):
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        pygame.display.set_caption('Bomberman')
        self.font: pygame.font.Font = pygame.font.Font('PixelifySansFont/PixelifySans-VariableFont_wght.ttf', 80)
        self.start_menu_surface: pygame.Surface = pygame.image.load(
            'assets/Menu/menu_background.png').convert_alpha()
        self.start_text_white = self.font.render('START', True, (255, 255, 255))
        self.start_text_hovered = self.font.render('START', True, (255, 127, 39))
        self.is_hovered = False
         
    def __initialize_objects(self):
        self.start_rect = self.start_text_white.get_rect()
        self.start_rect.center = (380, 160)
        self.screen.blit(self.start_menu_surface, (0, 0))
        if self.is_hovered:
                self.screen.blit(self.start_text_hovered, self.start_rect)
        else:
            self.screen.blit(self.start_text_white, self.start_rect)

    def handle_mouse_hover(self, mouse_pos):
        self.is_hovered = self.start_rect.collidepoint(mouse_pos)
        
    
    def run(self):
        start: bool = False
        while not start:
            self.__initialize_objects()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    self.handle_mouse_hover(event.pos)
                elif event.type == MOUSEBUTTONDOWN:
                    if self.is_hovered:
                        start = True
        game: Game = Game()
        game.run()