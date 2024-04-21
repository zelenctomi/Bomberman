import pygame


class Scoreboard:

    SCREEN_WIDTH: int = 750
    SCREEN_HEIGHT: int = 700

    def __init__(self, screen_param):
        self.screen_param = screen_param
        pygame.init()
        self.__load_asset()
        self.__write_datas()
        self.__render()

    def __load_asset(self):
        self.scoreboard_surface: pygame.Surface = pygame.image.load(
            'Assets/Menu/Status_Bar.png').convert_alpha()

    def __render(self):
        self.screen_param.blit(self.scoreboard_surface, (0, 650))

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

        self.screen_param.blit(player_1, player_1_rect)
        self.screen_param.blit(player_2, player_2_rect)
        self.screen_param.blit(player_3, player_3_rect)
