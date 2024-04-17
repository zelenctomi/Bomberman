import pygame

class Scoreboard:

    SCREEN_WIDTH: int = 750
    SCREEN_HEIGHT: int = 700

    def __init__(self, screen_param):
        pygame.init()
        self.__load_asset()
        self.__render(screen_param)

    def __load_asset(self):
        self.scoreboard_surface: pygame.Surface = pygame.image.load(
            'Assets/Menu/Status_Bar.png').convert_alpha()

    def __render(self, screen_param):
        screen_param.blit(self.scoreboard_surface, (0, 650))