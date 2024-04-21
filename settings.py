import pygame


class Settings:
  # Map Settings #
  BACKGROUND: tuple[int, int, int] = (222, 172, 245)
  SCREEN_WIDTH: int = 750
  SCREEN_HEIGHT: int = 700
  WIDTH: int = 15 # Map width in blocks
  HEIGHT: int = 13 # Map height in blocks
  BLOCK_SIZE: int = 50
  POWERUP_SIZE: int = 30
  POWERUP_OFFSET: int = (BLOCK_SIZE - POWERUP_SIZE) // 2

  # Framerate #
  FPS: int = 60
  ANIMATION_FPS: int = 15

  # Player Settings #
  P1_CONTROLS: dict[str, int] = {'left': pygame.K_a, 'right': pygame.K_d,
                                 'up': pygame.K_w, 'down': pygame.K_s, 'place': pygame.K_SPACE}
  P2_CONTROLS: dict[str, int] = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                                 'up': pygame.K_UP, 'down': pygame.K_DOWN, 'place': pygame.K_RETURN}
  P3_CONTROLS: dict[str, int] = {'left': pygame.K_j, 'right': pygame.K_l,
                                 'up': pygame.K_i, 'down': pygame.K_k, 'place': pygame.K_o}

  # These colors are subtracted from the original to create new ones
  P2_COLOR: tuple[int, int, int] = (50, 0, 75)
  P3_COLOR: tuple[int, int, int] = (90, 0, 0)

  # Bomb Settings #
  BOMB_TIMER: int = 3 # Seconds
  BOMB_FRAMES: int = 12