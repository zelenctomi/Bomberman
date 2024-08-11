from fields import *
from spawner import *
from scoreboard import *
from gameover import *
from settings import Settings
import sys


class Game:
  TARGET_ENTITY_FRAME: int = Settings.FPS // Settings.ANIMATION_FPS
  TARGET_BOMB_FRAME: int = Settings.FPS // Settings.BOMB_FRAMES * Settings.BOMB_TIMER

  def __init__(self, player_count: int, level: int, rounds: int = 2):
    pygame.init()
    pygame.display.set_caption('Bomberman')
    self.screen: pygame.Surface = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    self.clock: pygame.time.Clock = pygame.time.Clock()
    self.font: pygame.font.Font = pygame.font.Font(Settings.FONT, 16)
    self.level: int = level
    self.rounds: int = rounds
    self.running: bool = True
    # Game objects #
    self.scoreboard: Scoreboard = Scoreboard(self.screen, player_count)
    self.gameover: Gameover = Gameover(self.screen)
    self.fields: Fields = Fields()
    self.fields.load_map(level)
    self.spawner: Spawner = Spawner(self.fields)
    self.players: list[Player] = self.spawner.spawn_players(player_count)
    self.monsters: list[Monster] = self.spawner.spawn_monsters(5)
    # Animation #
    self.entity_frame_trigger: int = 0
    self.bomb_frame_trigger: int = 0

  def __load_assets(self) -> None:
    '''
    Loads textures for game objects
    '''
    for player in self.players:
      player.load_assets(self.players.index(player) + 1)
    for monster in self.monsters:
      monster.load_assets()

    self.bomb_assets: list[pygame.Surface] = [pygame.image.load(f'Assets/Bomb/b{i}.png').convert_alpha() for i in range(1, 13)]
    self.explosion_assets: list[pygame.Surface] = [pygame.image.load(f'Assets/Bomb/e{i}.png').convert_alpha() for i in range(1, 13)]
    self.wall_asset: pygame.Surface = pygame.image.load('Assets/Walls/Default/wall.png').convert_alpha()
    self.crumbly_asset: pygame.Surface = pygame.image.load('Assets/Walls/Default/crumbly.png').convert_alpha()
    self.barricade_asset: pygame.Surface = pygame.image.load('Assets/Walls/Default/barricade.png').convert_alpha()
    # Powerups #
    self.extra_bomb_surface: pygame.Surface = pygame.image.load('Assets/Powerups/extra_bomb.png').convert_alpha()
    self.longer_explosion_surface: pygame.Surface = pygame.image.load('Assets/Powerups/longer_explosion.png').convert_alpha()
    self.detonator_surface: pygame.Surface = pygame.image.load('Assets/Powerups/detonator.png').convert_alpha()
    self.invulnerability_surface: pygame.Surface = pygame.image.load('Assets/Powerups/invulnerability.png').convert_alpha()
    self.speed_surface: pygame.Surface = pygame.image.load('Assets/Powerups/speed.png').convert_alpha()
    self.barricade_surface: pygame.Surface = pygame.image.load('Assets/Powerups/barricade.png').convert_alpha()
    self.ghost_surface: pygame.Surface = pygame.image.load('Assets/Powerups/ghostwalk.png').convert_alpha()

  def __render_map(self) -> None:
    '''
    Pairs the textures with corresponding game objects, then
    renders the map. If there are no more runs then renders the
    gameover screen
    '''
    self.screen.fill(Settings.BACKGROUND)
    for wall in self.fields.walls:
      if isinstance(wall, Crumbly_wall):
        self.screen.blit(self.crumbly_asset, wall.rect)
      elif isinstance(wall ,Barricade_wall):
        self.screen.blit(self.barricade_asset, wall.rect)
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
      if monster.alive:
        self.screen.blit(monster.surface, monster.rect)

    for player in self.players:
      self.screen.blit(player.surface, player.rect)

    self.scoreboard.render()

    if self.rounds < 1:
      self.gameover.render()

  def __move_entities(self) -> None:
    '''
    Moves monsters and moves players if it is not gameove yet
    '''
    for monster in self.monsters:
      monster.move()
    if self.rounds > 0:
      for player in self.players:
        player.move()

  def __update_extra_powerups(self):
    for player in self.players:
      player.check_extra_powerups()

  def __update_frames(self) -> None:
    '''
    This method updates entity frames.
    Animation FPS is set by Settings.ANIMATION_FPS.
    The animation FPS is independent of the Settings.FPS.
    '''
    # self.scoreboard.slide()
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
    '''
    Indirectly removes expired explosions, then checks if the players or monsters collide
    with an explosion, in which case they die. Checks if an explosion hits a bomb. If so,
    then sets the bomb timer to 0.
    '''
    self.fields.update_explosions()
    for explosion in self.fields.explosions:
      for player in self.players:
        if pygame.Rect.colliderect(player.rect, explosion.rect):
          player.die()
      for monster in self.monsters:
        if pygame.Rect.colliderect(monster.rect, explosion.rect):
          monster.die()
      for bomb in self.fields.bombs:
        if pygame.Rect.colliderect(explosion.rect, bomb.rect):
          bomb.update(0)

  def __handle_entity_collision(self) -> None:
    '''
    Checks if monsters collide with players. If so, then kills the affected players
    '''
    for monster in self.monsters:
      if monster.alive:
        for player in self.players:
          if pygame.Rect.colliderect(player.rect, monster.hitbox):
            player.die()

  def __handle_game_over(self) -> None:
    '''
    Counts the living players then if less than 2 are alive and
    no bombs are active, then initiates the gameover event
    '''
    alive_players: int = 0
    for player in self.players:
      if player.alive:
        alive_players += 1
    if self.fields.no_bombs_active() and alive_players < 2:
      self.__game_over()

  def __game_over(self) -> None:
    '''
    Decrements the number of rounds and updates the scoreboard.
    If there are rounds left, then starts a new round. Else the game
    returns to the main menu
    '''
    if self.rounds > 0:
      self.rounds -= 1
      self.__update_winner_score()
      
    if self.rounds > 0:
      self.__start_new_round()
    else:
      self.__handle_proceed_to_menu()

  def __start_new_round(self) -> None:
    '''
    Starts a new round by reloading the map and
    respawning the players and monsters
    '''
    self.fields.reload_map(self.level)
    self.spawner.respawn_players(self.players)
    self.spawner.respawn_monsters(self.monsters)

  def __update_winner_score(self) -> None:
    '''
    Updates the scoreboard for every living player
    '''
    for player in self.players:
      if player.alive:
        self.scoreboard.update(self.players.index(player))

  def __handle_proceed_to_menu(self) -> None:
    '''
    If the gameover event happens and a key is pressed,
    then stops the game loop
    '''
    if self.gameover.proceed and any(pygame.key.get_pressed()):
      # self.running = False
      pass

  def run(self) -> None:
    '''
    The main game loop. Loads assets and loops through the following:
    renders the map, moves the players and monsters, updates the animation,
    updates the explosions and the events they cause, checks for collisions,
    updates bomb lifetime, checks for gameover, updates the display and ticks the
    game clock based on set FPS.
    '''
    self.__load_assets()
    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
          pygame.quit()
          sys.exit()

      self.__render_map()
      self.__move_entities()
      self.__update_frames()
      self.__update_extra_powerups()
      self.__handle_explosions()
      self.__handle_entity_collision()
      self.fields.update_bombs()
      self.__handle_game_over()

      pygame.display.update()
      self.clock.tick(Settings.FPS)
