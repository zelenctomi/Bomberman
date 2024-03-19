import pygame
import random
from wall import Wall
from crumbly_wall import Crumbly_wall
from player import Player
from bomb import Bomb
from explosion import Explosion
from extra_bomb import Extra_bomb
from longer_explosion import Longer_explosion
from monster import Monster

class Game:
  SCREEN_WIDTH = 750
  SCREEN_HEIGHT = 650

  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
    pygame.display.set_caption('Bomberman')
    self.clock = pygame.time.Clock()

    self.load_assets()
    self.initialize_objects()

  def load_assets(self):
    self.player1_surface = pygame.image.load('assets/player1.png').convert()
    self.player2_surface = pygame.image.load('assets/player2.png').convert()
    self.dead_surface1 = pygame.image.load('assets/dead_player1.png').convert()
    self.dead_surface2 = pygame.image.load('assets/dead_player2.png').convert()
    self.crumbly_wall_surface = pygame.image.load('assets/crumbly_wall.png').convert()
    self.wall_surface = pygame.image.load('assets/wall.png').convert()
    self.bomb_surface = pygame.image.load('assets/bomb.png').convert()
    self.bomb_surface.set_colorkey((0, 200, 0))
    self.explosion_surface = pygame.image.load('assets/explosion_center.png').convert()
    self.explosion_surface.set_colorkey((0, 200, 0))
    self.extra_bomb_surface = pygame.image.load('assets/extra_bomb.png').convert()
    self.extra_bomb_surface.set_colorkey((0, 200, 0))
    self.longer_explosion_surface = pygame.image.load('assets/longer_explosion.png').convert()
    self.longer_explosion_surface.set_colorkey((0, 200, 0))
    self.monster_surface = pygame.image.load('assets/monster.png').convert()
    self.monster_surface.set_colorkey((0, 200, 0))

  def initialize_objects(self):
    self.player1 = Player(50, 50, self.player1_surface, self.dead_surface1)
    self.player2 = Player(675, 575, self.player2_surface, self.dead_surface2)
    self.players = [self.player1, self.player2]
    self.bombs = []
    self.explosions = []
    self.walls = []
    self.crumbly_walls = []
    self.powerups = []
    self.monsters = []
    self.game_lapse_time = 0
    self.fields = [[[] for _ in range(15)] for _ in range(13)]

  def get_objects_at_coords(self, x, y):
    row_index = y // 50
    column_index = x // 50
    return self.fields[row_index][column_index]

  def get_objects_at_object(self, obj):
    potential_collisons = []
    for corner in [(obj.rect.topleft[0], obj.rect.topleft[1]), (obj.rect.topright[0], obj.rect.topright[1]),
             (obj.rect.bottomleft[0], obj.rect.bottomleft[1]), (obj.rect.bottomright[0], obj.rect.bottomright[1])]:
      for list_element in self.get_objects_at_coords(corner[0], corner[1]):
        if list_element not in potential_collisons:
          potential_collisons.append(list_element)
    return sum([potential_collisons], [])

  def field_has_bomb(self, x, y):
    for list_element in self.get_objects_at_coords(x, y):
      if isinstance(list_element, Bomb):
        return True
    return False

  def spawn_walls(self):
    wall_start_x = 0
    for x in range(15):
      wall_start_y = 0
      for y in range(13):
        if wall_start_x in [0, 700] or wall_start_y in [0, 600] or \
            (wall_start_x in [100, 200, 300, 400, 500, 600] and wall_start_y in [100, 200, 300, 400, 500]):
          wall_instance = Wall(wall_start_x, wall_start_y)
          self.walls.append(wall_instance)
          self.fields[y][x].append(wall_instance)
        wall_start_y += 50
      wall_start_x += 50

  def spawn_crumbly_walls(self):
    forbidden_crumbly_wall_spots = [[50, 50], [50, 100], [100, 50], [650, 550], [600, 550], [650, 500]]
    crumbly_wall_start_x = 50
    for x in range(13):
      crumbly_wall_start_y = 50
      for y in range(11):
        if (crumbly_wall_start_x in [100, 200, 300, 400, 500, 600] and crumbly_wall_start_y not in [100, 200, 300, 400, 500]) and \
            [crumbly_wall_start_x, crumbly_wall_start_y] not in forbidden_crumbly_wall_spots and random.randint(0, 9) > 7:
          crumbly_wall_instance = Crumbly_wall(crumbly_wall_start_x, crumbly_wall_start_y)
          self.crumbly_walls.append(crumbly_wall_instance)
          self.fields[y + 1][x + 1].append(crumbly_wall_instance)
        crumbly_wall_start_y += 50
      crumbly_wall_start_x += 50

  def move_or_collide(self, player_param, x, y):
    player_param.rect.x += x * (self.game_lapse_time / 1000)
    player_param.rect.y += y * (self.game_lapse_time / 1000)

    potential_collisons = self.get_objects_at_object(player_param)

    for obj in potential_collisons:
      if isinstance(obj, (Wall, Crumbly_wall)) and pygame.Rect.colliderect(player_param.rect, obj.rect):
        player_param.rect.x -= x * (self.game_lapse_time / 1000)
        player_param.rect.y -= y * (self.game_lapse_time / 1000)
      elif isinstance(obj, Extra_bomb):
        player_param.max_bomb_count += 1
        self.get_objects_at_coords(obj.rect.x, obj.rect.y).remove(obj)
        self.powerups.remove(obj)
      elif isinstance(obj, Longer_explosion):
        player_param.explosion_length += 1
        self.get_objects_at_coords(obj.rect.x, obj.rect.y).remove(obj)
        potential_collisons.remove(obj)
        self.powerups.remove(obj)

    for bomb_obj in self.bombs:
      if not bomb_obj.stood_on and pygame.Rect.colliderect(player_param.rect, bomb_obj.rect):
        player_param.rect.x -= 2 * x
        player_param.rect.y -= 2 * y

  def render_map(self):
    self.screen.fill((0, 200, 0))

    for wall_obj in self.walls:
      self.screen.blit(self.wall_surface, wall_obj)

    for crumbly_wall_obj in self.crumbly_walls:
      self.screen.blit(self.crumbly_wall_surface, crumbly_wall_obj)

    for bomb_instance in self.bombs:
      self.screen.blit(self.bomb_surface, bomb_instance)

    for explosion_instance in self.explosions:
      self.screen.blit(self.explosion_surface, explosion_instance)

    for powerup_instance in self.powerups:
      if isinstance(powerup_instance, Extra_bomb):
        self.screen.blit(self.extra_bomb_surface, powerup_instance)
      elif isinstance(powerup_instance, Longer_explosion):
        self.screen.blit(self.longer_explosion_surface, powerup_instance)

    for player in self.players:
      if player.is_alive:
        self.screen.blit(player.surface, player.rect)
      else:
        self.screen.blit(player.dead_surface, player.rect)

    for monster_instance in self.monsters:
      if monster_instance.is_alive:
        self.screen.blit(self.monster_surface, monster_instance.rect)

  def move_player1(self):
    if self.player1.is_alive:
      key = pygame.key.get_pressed()
      if key[pygame.K_SPACE] and self.player1.bombs_deployed < self.player1.max_bomb_count \
          and not self.field_has_bomb(self.player1.rect.x + 10, self.player1.rect.y + 10):
        bomb_instance = Bomb((self.player1.rect.x + 10) - ((self.player1.rect.x + 10) % 50),
                   (self.player1.rect.y + 10) - ((self.player1.rect.y + 10) % 50), self.player1)
        self.bombs.append(bomb_instance)
        self.get_objects_at_coords(self.player1.rect.x + 10, self.player1.rect.y + 10).append(bomb_instance)
        self.player1.bombs_deployed += 1

      if key[pygame.K_a]:
        self.move_or_collide(self.player1, -300, 0)
      if key[pygame.K_d]:
        self.move_or_collide(self.player1, 300, 0)
      if key[pygame.K_w]:
        self.move_or_collide(self.player1, 0, -300)
      if key[pygame.K_s]:
        self.move_or_collide(self.player1, 0, 300)

      self.player1.rect.clamp_ip(self.screen.get_rect())

  def move_player2(self):
    if self.player2.is_alive:
      key = pygame.key.get_pressed()
      if key[pygame.K_o] and self.player2.bombs_deployed < self.player2.max_bomb_count \
          and not self.field_has_bomb(self.player2.rect.x + 10, self.player2.rect.y + 10):
        bomb_instance = Bomb((self.player2.rect.x + 10) - ((self.player2.rect.x + 10) % 50),
                   (self.player2.rect.y + 10) - ((self.player2.rect.y + 10) % 50), self.player2)
        self.bombs.append(bomb_instance)
        self.get_objects_at_coords(self.player2.rect.x + 10, self.player2.rect.y + 10).append(bomb_instance)
        self.player2.bombs_deployed += 1

      if key[pygame.K_LEFT]:
        self.move_or_collide(self.player2, -300, 0)
      if key[pygame.K_RIGHT]:
        self.move_or_collide(self.player2, 300, 0)
      if key[pygame.K_UP]:
        self.move_or_collide(self.player2, 0, -300)
      if key[pygame.K_DOWN]:
        self.move_or_collide(self.player2, 0, 300)

      self.player2.rect.clamp_ip(self.screen.get_rect())

  def turn_monster_if_obstacle(self, monster_instance, collision_object):
    if pygame.Rect.colliderect(monster_instance.rect, collision_object.rect):
      monster_instance.rect.x -= monster_instance.x_direction
      monster_instance.rect.y -= monster_instance.y_direction
      if monster_instance.lapse > 150:
        monster_instance.change_direction_randomly()
        return True
      monster_instance.x_direction = monster_instance.x_direction * (-1)
      monster_instance.y_direction = monster_instance.y_direction * (-1)
      return True
    return False

  def move_monsters(self):
    for monster_instance in self.monsters:
      if monster_instance.lapse == 0:
        monster_instance.change_direction_randomly()
        monster_instance.lapse = random.randint(400, 1600)
      else:
        monster_instance.lapse -= 1
        monster_instance.rect.x += monster_instance.x_direction
        monster_instance.rect.y += monster_instance.y_direction

        potential_collisions = self.get_objects_at_object(monster_instance)
        for obj in potential_collisions:
          if isinstance(obj, (Wall, Crumbly_wall, Bomb)):
            if self.turn_monster_if_obstacle(monster_instance, obj):
              return
        for player in self.players:
          if pygame.Rect.colliderect(player.rect, monster_instance.rect):
            player.player_died()

  def spawn_powerup(self, x, y):
    if random.randint(0, 9) > 5:
      if random.randint(0, 9) > 4:
        extrabomb_instance = Extra_bomb(x, y)
        self.powerups.append(extrabomb_instance)
        self.get_objects_at_coords(x, y).append(extrabomb_instance)
      else:
        longerexplosion_instance = Longer_explosion(x, y)
        self.powerups.append(longerexplosion_instance)
        self.get_objects_at_coords(x, y).append(longerexplosion_instance)

  def remove_destroyed_entities(self):
    for crumbly_wall_instance in self.crumbly_walls:
      if crumbly_wall_instance.destroyed:
        self.get_objects_at_coords(crumbly_wall_instance.rect.x, crumbly_wall_instance.rect.y).remove(
          crumbly_wall_instance)
        self.crumbly_walls.remove(crumbly_wall_instance)
        self.spawn_powerup(crumbly_wall_instance.rect.x, crumbly_wall_instance.rect.y)
    for monster_instance in self.monsters:
      if not monster_instance.is_alive:
        self.monsters.remove(monster_instance)

  def handle_explosion(self):
    for explosion_instance in self.explosions:
      if explosion_instance.lifetime > 0:
        explosion_instance.lifetime -= 1
      else:
        self.explosions.remove(explosion_instance)
    for explosion_instance in self.explosions:
      for player in self.players:
        if pygame.Rect.colliderect(player.rect, explosion_instance.rect):
          player.player_died()
      for monster_instance in self.monsters:
        if pygame.Rect.colliderect(monster_instance.rect, explosion_instance.rect):
          monster_instance.is_alive = False
      for bomb_instance in self.bombs:
        if pygame.Rect.colliderect(explosion_instance.rect, bomb_instance.rect):
          self.explosions.append(Explosion(explosion_instance.rect.x, explosion_instance.rect.y))
          self.explosions[-1].explode(bomb_instance.owner.explosion_length, self)
          self.get_objects_at_coords(explosion_instance.rect.x, explosion_instance.rect.y).remove(bomb_instance)
          self.bombs.remove(bomb_instance)
          bomb_instance.owner.bombs_deployed -= 1

  def handle_bombs(self):
    for bomb_instance in self.bombs:
      if bomb_instance.fuse_time > 0:
        bomb_instance.fuse_time -= 1
      else:
        self.explosions.append(Explosion(bomb_instance.rect.x, bomb_instance.rect.y))
        self.explosions[-1].explode(bomb_instance.owner.explosion_length, self)
        self.get_objects_at_coords(bomb_instance.rect.x, bomb_instance.rect.y).remove(bomb_instance)
        self.bombs.remove(bomb_instance)
        bomb_instance.owner.bombs_deployed -= 1

  def spawn_monsters(self, count):
    forbidden_monster_spots = [[50, 50], [50, 100], [100, 50], [650, 550], [600, 550], [650, 500]]
    for _ in range(count):
      can_spawn = False
      while not can_spawn:
        spawn_x = random.randint(1, 13) * 50
        spawn_y = random.randint(1, 11) * 50
        spawn_x += random.randint(0, 24)
        spawn_y += random.randint(0, 24)
        if [spawn_x, spawn_y] in forbidden_monster_spots:
          continue
        can_spawn = True
        for crumbly_wall_instance in self.crumbly_walls:
          if crumbly_wall_instance.rect.collidepoint(spawn_x, spawn_y):
            can_spawn = False
        for wall_instance in self.walls:
          if wall_instance.rect.collidepoint(spawn_x, spawn_y):
            can_spawn = False
      self.monsters.append(Monster(spawn_x, spawn_y))

  def update_bomb_trampling(self):
    for bomb_instance in self.bombs:
      bomb_instance.stood_on = False
      if pygame.Rect.colliderect(self.player1.rect, bomb_instance.rect):
        bomb_instance.stood_on = True
      elif pygame.Rect.colliderect(self.player2.rect, bomb_instance.rect):
        bomb_instance.stood_on = True
    return

  def tick_explosion(self):
    if Explosion.delay > 0:
      Explosion.delay -= 1
    else:
      Explosion.delay = 50

  def run(self):
    self.spawn_walls()
    self.spawn_crumbly_walls()
    self.spawn_monsters(1)
    run = True
    while run:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False

      self.render_map()
      self.update_bomb_trampling()
      self.move_monsters()
      self.move_player1()
      self.move_player2()
      self.handle_explosion()
      self.handle_bombs()
      self.remove_destroyed_entities()
      self.tick_explosion()

      pygame.display.update()
      self.clock.tick(150)
      self.game_lapse_time = self.clock.get_time()

# Starting the Game
game = Game()
game.run()
