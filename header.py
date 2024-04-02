import pygame
import sys
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WINDOW_WIDTH = 750

header_font = pygame.font.SysFont(None, 36)
menu_font = pygame.font.SysFont(None, 24)

players_points = {'Player 1': 0, 'Player 2': 0}

class Menu:
    
    def __init__(self, window):
        pygame.init()
        self.window = window
        self.menu_items = ['Start', 'Stop', 'Exit']
        self.selected_menu_item = 0
        self.start_ticks = None
        self.stopped_time = 0
        self.running = False

    def draw(self):
        self.window.fill(WHITE)
        self.draw_menu()
        self.draw_status()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_menu_item = (self.selected_menu_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_menu_item = (self.selected_menu_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                if self.selected_menu_item == 0:
                    self.start()
                elif self.selected_menu_item == 1:
                    self.stop()
                elif self.selected_menu_item == 2:
                    pygame.quit()
                    sys.exit()

    def draw_menu(self):
        for i, item in enumerate(self.menu_items):
            color = BLACK if i == self.selected_menu_item else WHITE
            text = menu_font.render(item, True, color)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, 100 + i * 40))
            self.window.blit(text, rect)

    def draw_status(self):
        if self.start_ticks is not None:
            if self.stopped_time == 0:
                elapsed_time = pygame.time.get_ticks() - self.start_ticks
            else:
                elapsed_time = self.stopped_time
        else:
            elapsed_time = 0

        stopper_text = header_font.render(f'Stopper: {elapsed_time / 1000:.2f} sec', True, BLACK)
        self.window.blit(stopper_text, (50, 20))

        players_text = header_font.render(f'Points: {players_points}', True, BLACK)
        self.window.blit(players_text, (50, 50))

    def start(self):
        self.start_ticks = pygame.time.get_ticks()
        self.running = True

    def stop(self):
        if self.running:
            self.stopped_time = pygame.time.get_ticks() - self.start_ticks
            self.running = False

