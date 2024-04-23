from fields import *
from spawner import *
from scoreboard import *
from settings import Settings


class Game:
  TARGET_ENTITY_FRAME: int = Settings.FPS // Settings.ANIMATION_FPS
  TARGET_BOMB_FRAME: int = Settings.FPS // Settings.BOMB_FRAMES * Settings.BOMB_TIMER

  def __init__(self, player_count: int, level: int):
    self.player_count: int = player_count
    self.level: int = level
    pygame.init()
    pygame.display.set_caption('Bomberman')
    self.screen: pygame.Surface = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    self.clock: pygame.time.Clock = pygame.time.Clock()
    self.font: pygame.font.Font = pygame.font.Font(Settings.FONT, 16)

  def __load_assets(self) -> None:
    for player in self.players:
      player.load_assets(self.players.index(player) + 1)
    for monster in self.monsters:
      monster.load_assets()

    self.bomb_assets: list[pygame.Surface] = [pygame.image.load(f'Assets/Bomb/b{i}.png').convert_alpha() for i in range(1, 13)]
    self.explosion_assets: list[pygame.Surface] = [pygame.image.load(f'Assets/Bomb/e{i}.png').convert_alpha() for i in range(1, 13)]
    self.wall_asset: pygame.Surface = pygame.image.load('Assets/Walls/Default/wall.png').convert_alpha()
    self.crumbly_asset: pygame.Surface = pygame.image.load('Assets/Walls/Default/crumbly.png').convert_alpha()
    self.barricade_asset: pygame.Surface = pygame.image.load('Assets/Walls/Default/barricade.png').convert_alpha()
    self.scoreboard_surface: pygame.Surface = pygame.image.load('Assets/Menu/Status_Bar.png').convert_alpha()
    # Powerups #
    self.extra_bomb_surface: pygame.Surface = pygame.image.load('Assets/Powerups/extra_bomb.png').convert_alpha()
    self.longer_explosion_surface: pygame.Surface = pygame.image.load('Assets/Powerups/longer_explosion.png').convert_alpha()
    self.detonator_surface: pygame.Surface = pygame.image.load('Assets/Powerups/detonator.png').convert_alpha()
    self.invulnerability_surface: pygame.Surface = pygame.image.load('Assets/Powerups/invulnerability.png').convert_alpha()
    self.speed_surface: pygame.Surface = pygame.image.load('Assets/Powerups/speed.png').convert_alpha()
    self.barricade_surface: pygame.Surface = pygame.image.load('Assets/Powerups/barricade.png').convert_alpha()
    self.ghost_surface: pygame.Surface = pygame.image.load('Assets/Powerups/ghostwalk.png').convert_alpha()


  def __initialize_objects(self) -> None:
    self.entity_frame_trigger: int = 0
    self.bomb_frame_trigger: int = 0
    self.scoreboard: Scoreboard = Scoreboard(self.screen)
    self.fields: Fields = Fields()
    self.fields.load_map(self.level)
    self.spawner: Spawner = Spawner(self.fields)
    self.players: list[Player] = self.spawner.spawn_players(self.player_count)
    self.monsters: list[Monster] = self.spawner.spawn_monsters(3)

  def __render_map(self) -> None:
    self.screen.fill(Settings.BACKGROUND)

    for wall in self.fields.walls:
      if isinstance(wall, Crumbly_wall):
        self.screen.blit(self.crumbly_asset, wall.rect)
      ##
      elif isinstance(wall ,Wall):
        self.screen.blit(self.wall_asset, wall.rect)

    for bomb in self.fields.bombs:
      self.screen.blit(bomb.surface, bomb.rect)

    for explosion in self.fields.explosions:
      self.screen.blit(self.explosion_assets[2], explosion.rect)

    for powerup in self.fields.powerups:
      if isinstance(powerup, Extra_bomb):
        self.screen.blit(self.extra_bomb_surface, powerup.rect)
      elif isinstance(powerup, Longer_explosion):
        self.screen.blit(self.longer_explosion_surface, powerup.rect)
      elif isinstance(powerup, Detonator):
        self.screen.blit(self.detonator_surface, powerup.rect)
      elif isinstance(powerup, Invulnerability):
        self.screen.blit(self.invulnerability_surface, powerup.rect)
      elif isinstance(powerup, Speed):
        self.screen.blit(self.speed_surface, powerup.rect)
      elif isinstance(powerup, Barricade):
        self.screen.blit(self.barricade_surface, powerup.rect)
      elif isinstance(powerup, Ghost):
        self.screen.blit(self.ghost_surface, powerup.rect)

    for monster in self.monsters:
      if monster.is_alive:
        self.screen.blit(monster.surface, monster.rect)

    for player in self.players:
        self.screen.blit(player.surface, player.rect)
      
    self.screen.blit(self.scoreboard_surface, (0, 635)) # TODO: Create a constant in Settings

  def __move_entities(self) -> None:
    for monster in self.monsters:
      monster.move()
    for player in self.players:
      player.move()

  def __update_frames(self) -> None:
    '''
    This method updates entity frames.
    Animation FPS is set by Settings.ANIMATION_FPS.
    The animation FPS is independent of the Settings.FPS.
    '''
    self.entity_frame_trigger += 1
    self.bomb_frame_trigger += 1
    if self.entity_frame_trigger == Game.TARGET_ENTITY_FRAME:
      for player in self.players:
        player.update_frame()
      for monster in self.monsters:
        monster.update_frame()
      self.entity_frame_trigger = 0
    if self.bomb_frame_trigger == Game.TARGET_BOMB_FRAME:
      for bomb in self.fields.bombs:
        bomb.update_frame()
        bomb.update_surface(self.bomb_assets[bomb.frame])
      self.bomb_frame_trigger = 0

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

  def __update_extra_powerups(self):
    for player in self.players:
      player.check_extra_powerups()

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
      self.__update_extra_powerups()
      self.__handle_explosions()
      self.__handle_death()
      self.fields.update_bombs()

      pygame.display.update()
      self.clock.tick(Settings.FPS)
