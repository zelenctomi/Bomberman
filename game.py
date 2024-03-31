from fields import *
from spawner import *

class Game:
  BLOCK_SIZE: int = 50
  SCREEN_WIDTH: int = 750
  SCREEN_HEIGHT: int = 650
  P1_CONTROLS: dict[str, int] = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s, 'place': pygame.K_SPACE}
  P2_CONTROLS: dict[str, int] = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN, 'place': pygame.K_o}

  def __init__(self):
    pygame.init()
    pygame.display.set_caption('Bomberman')
    self.screen: pygame.Surface = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
    self.clock: pygame.Clock = pygame.time.Clock()

  def __load_assets(self) -> None:
    self.player1_surface: pygame.Surface = pygame.image.load(
      'assets/player1.png').convert()
    self.player2_surface: pygame.Surface = pygame.image.load(
      'assets/player2.png').convert()
    self.dead_surface1: pygame.Surface = pygame.image.load(
      'assets/dead_player1.png').convert()
    self.dead_surface2: pygame.Surface = pygame.image.load(
      'assets/dead_player2.png').convert()
    self.crumbly_wall_surface: pygame.Surface = pygame.image.load(
      'assets/crumbly_wall.png').convert()
    self.wall_surface: pygame.Surface = pygame.image.load(
      'assets/wall.png').convert()
    self.bomb_surface: pygame.Surface = pygame.image.load(
      'assets/bomb.png').convert()
    self.bomb_surface.set_colorkey((0, 200, 0))
    self.explosion_surface: pygame.Surface = pygame.image.load(
      'assets/explosion_center.png').convert()
    self.explosion_surface.set_colorkey((0, 200, 0))
    self.extra_bomb_surface: pygame.Surface = pygame.image.load(
      'assets/extra_bomb.png').convert()
    self.extra_bomb_surface.set_colorkey((0, 200, 0))
    self.longer_explosion_surface: pygame.Surface = pygame.image.load(
      'assets/longer_explosion.png').convert()
    self.longer_explosion_surface.set_colorkey((0, 200, 0))
    self.monster_surface: pygame.Surface = pygame.image.load(
      'assets/monster.png').convert()
    self.monster_surface.set_colorkey((0, 200, 0))

  def __initialize_objects(self) -> None:
    self.fields: Fields = Fields()
    self.fields.load_walls()
    self.fields.load_crumbly_walls()
    self.spawner: Spawner = Spawner(self.fields)
    self.players: list[Player] = self.spawner.spawn_players([Game.P1_CONTROLS, Game.P2_CONTROLS])
    self.players[0].draw(self.player1_surface, self.dead_surface1)
    self.players[1].draw(self.player2_surface, self.dead_surface2)
    self.monsters: list[Monster] = self.spawner.spawn_monsters(1)
    self.elapsed: int = 0

  def __render_map(self) -> None:
    self.screen.fill((0, 200, 0))

    for wall in self.fields.walls:
      if isinstance(wall, Crumbly_wall):
        self.screen.blit(self.crumbly_wall_surface, wall)
      else:
        self.screen.blit(self.wall_surface, wall)
    for bomb in self.fields.bombs:
      self.screen.blit(self.bomb_surface, bomb)
    for explosion in self.fields.explosions:
      self.screen.blit(self.explosion_surface, explosion)
    for powerup in self.fields.powerups:
      if isinstance(powerup, Extra_bomb):
        self.screen.blit(self.extra_bomb_surface, powerup)
      elif isinstance(powerup, Longer_explosion):
        self.screen.blit(self.longer_explosion_surface, powerup)
    for monster in self.monsters:
      if monster.is_alive:
        self.screen.blit(self.monster_surface, monster.rect)
    for player in self.players:
      if player.is_alive:
        self.screen.blit(player.surface, player.rect)
        # draw border around player
        # pygame.draw.rect(self.screen, (0, 0, 0), player.rect, 2)
      else:
        self.screen.blit(player.dead_surface, player.rect)

  def __move_entities(self) -> None:
    for monster in self.monsters:
      monster.move()
    for player in self.players:
      player.move()

  def __handle_explosions(self) -> None:
    self.fields.update_explosions()
    for explosion in self.fields.explosions:
      for player in self.players:
        if pygame.Rect.colliderect(player.rect, explosion.rect):
          player.die()
      for monster in self.monsters:
        if pygame.Rect.colliderect(monster.rect, explosion.rect):
          monster.die()
          self.monsters.remove(monster) # So the monster doesn't get drawn after death
      for bomb in self.fields.bombs:
        if pygame.Rect.colliderect(explosion.rect, bomb.rect):
          bomb.update(0)

  def run(self) -> None:
    self.__load_assets()
    self.__initialize_objects()
    # self.__move_entities() # DELETE THIS LINE
    run: bool = True
    while run:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False

      self.__render_map()
      self.__move_entities()
      self.__handle_explosions()
      self.fields.update_bombs()

      pygame.display.update()
      self.clock.tick(100)
      self.elapsed: int = self.clock.get_time()
