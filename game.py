from fields import *
from spawner import *
from scoreboard import *


class Game:
  BACKGROUND: tuple[int, int, int] = (222, 172, 245)
  BLOCK_SIZE: int = 50
  SCREEN_WIDTH: int = 750
  SCREEN_HEIGHT: int = 700
  FPS: int = 150
  ANIMATION_FPS: int = 20
  TARGET_ENTITY_FRAME: int = FPS // ANIMATION_FPS
  P1_CONTROLS: dict[str, int] = {'left': pygame.K_a, 'right': pygame.K_d,
                                 'up': pygame.K_w, 'down': pygame.K_s, 'place': pygame.K_SPACE}
  P2_CONTROLS: dict[str, int] = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                                 'up': pygame.K_UP, 'down': pygame.K_DOWN, 'place': pygame.K_RETURN}
  P3_CONTROLS: dict[str, int] = {'left': pygame.K_j, 'right': pygame.K_l,
                                 'up': pygame.K_i, 'down': pygame.K_k, 'place': pygame.K_o}

  def __init__(self):
    pygame.init()
    pygame.display.set_caption('Bomberman')
    self.screen: pygame.Surface = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
    self.clock: pygame.time.Clock = pygame.time.Clock()
    self.font: pygame.font.Font = pygame.font.Font('PixelifySansFont/PixelifySans-VariableFont_wght.ttf', 36)

  def __load_assets(self) -> None:
    for player in self.players:
      player.load_assets(self.players.index(player) + 1)

    self.crumbly_wall_surface: pygame.Surface = pygame.image.load(
      'Assets/Walls/Default/crumbly.png').convert_alpha()
    self.wall_surface: pygame.Surface = pygame.image.load(
      'Assets/Walls/Default/wall.png').convert_alpha()
    self.bomb_surface: pygame.Surface = pygame.transform.scale(pygame.image.load(
      'Assets/Bomb/bomb.png').convert_alpha(), (Game.BLOCK_SIZE, Game.BLOCK_SIZE))
    self.bomb_surface.set_colorkey((0, 200, 0))
    self.explosion_surface: pygame.Surface = pygame.image.load(
      'Assets/explosion_center.png').convert_alpha()
    # self.explosion_surface.set_colorkey((0, 200, 0))
    self.extra_bomb_surface: pygame.Surface = pygame.image.load(
      'Assets/extra_bomb.png').convert_alpha()
    # self.extra_bomb_surface.set_colorkey((0, 200, 0))
    self.longer_explosion_surface: pygame.Surface = pygame.image.load(
      'Assets/longer_explosion.png').convert_alpha()
    # self.longer_explosion_surface.set_colorkey((0, 200, 0))
    self.monster_surface: pygame.Surface = pygame.image.load(
      'Assets/monster.png').convert_alpha()
    # self.monster_surface.set_colorkey((0, 200, 0))
    self.scoreboard_surface: pygame.Surface = pygame.image.load(
      'Assets/Menu/Status_Bar.png').convert_alpha()

  def __initialize_objects(self) -> None:
    self.scoreboard: Scoreboard = Scoreboard(self.screen)
    self.entity_frame_trigger: int = 0
    self.fields: Fields = Fields()
    self.fields.load_walls()
    self.fields.load_crumbly_walls()
    self.spawner: Spawner = Spawner(self.fields)
    # self.players: list[Player] = self.spawner.spawn_players([Game.P1_CONTROLS, Game.P2_CONTROLS, Game.P3_CONTROLS])
    self.players: list[Player] = self.spawner.spawn_players([Game.P1_CONTROLS])
    self.monsters: list[Monster] = self.spawner.spawn_monsters(1)

  def __render_map(self) -> None:
    self.screen.fill(Game.BACKGROUND)

    for wall in self.fields.walls:
      if isinstance(wall, Crumbly_wall):
        self.screen.blit(self.crumbly_wall_surface, wall.rect)
        self.screen.blit(self.crumbly_wall_surface, wall.rect)
      else:
        self.screen.blit(self.wall_surface, wall.rect)
    for bomb in self.fields.bombs:
      self.screen.blit(self.bomb_surface, bomb.rect)
    for explosion in self.fields.explosions:
      self.screen.blit(self.explosion_surface, explosion.rect)
    for powerup in self.fields.powerups:
      if isinstance(powerup, Extra_bomb):
        self.screen.blit(self.extra_bomb_surface, powerup.rect)
      elif isinstance(powerup, Longer_explosion):
        self.screen.blit(self.longer_explosion_surface, powerup.rect)
    for monster in self.monsters:
      if monster.is_alive:
        self.screen.blit(self.monster_surface, monster.rect)
    for player in self.players:
      if player.is_alive:
        self.screen.blit(player.surface, player.rect)
      
    self.screen.blit(self.scoreboard_surface, (0, 635))

  def __move_entities(self) -> None:
    for monster in self.monsters:
      monster.move()
    for player in self.players:
      player.move()

  def __update_frames(self) -> None:
    '''
    This method updates entity frames.
    Animation FPS is set by Game.ANIMATION_FPS.
    The animation FPS is independent of the Game.FPS.
    '''
    self.entity_frame_trigger += 1
    if self.entity_frame_trigger == Game.TARGET_ENTITY_FRAME:
      for player in self.players:
        player.update_frame()
      self.entity_frame_trigger = 0

  def __handle_explosions(self) -> None:
    self.fields.update_explosions()
    for explosion in self.fields.explosions:
      for player in self.players:
        if pygame.Rect.colliderect(player.rect, explosion.rect):
          player.die()
      for monster in self.monsters:
        if pygame.Rect.colliderect(monster.rect, explosion.rect):
          monster.die()
          self.monsters.remove(monster)  # So the monster doesn't get drawn after death
      for bomb in self.fields.bombs:
        if pygame.Rect.colliderect(explosion.rect, bomb.rect):
          bomb.update(0)

  def __handle_death(self) -> None:
    for monster in self.monsters:
      for player in self.players:
        if pygame.Rect.colliderect(player.rect, monster.rect):
          player.die()

  def run(self) -> None:
    self.__initialize_objects()
    self.__load_assets()
    run: bool = True
    while run:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False

      self.__render_map()
      self.__move_entities()
      self.__update_frames()
      self.__handle_explosions()
      self.__handle_death()
      self.fields.update_bombs()

      pygame.display.update()
      self.clock.tick(Game.FPS)
