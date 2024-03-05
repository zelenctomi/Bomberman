import pygame
import random

from wall import wall
from crumbly_wall import crumbly_wall
from player import player
from bomb import bomb
from explosion import explosion
from extra_bomb import extra_bomb
from longer_explosion import longer_explosion
from monster import monster

pygame.init()
class Game:
    SCREEN_WIDTH = 750
    SCREEN_HEIGHT = 650
    # loading assets
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player1_surface = pygame.image.load('player1.png').convert()
    player2_surface = pygame.image.load('player2.png').convert()
    dead_surface1 = pygame.image.load('dead_player1.png').convert()
    dead_surface2 = pygame.image.load('dead_player2.png').convert()
    crumbly_wall_surface = pygame.image.load('crumbly_wall.png').convert()
    wall_surface = pygame.image.load('wall.png').convert()
    bomb_surface = pygame.image.load('bomb.png').convert()
    bomb_surface.set_colorkey((0,200,0))
    explosion_surface = pygame.image.load('explosion_center.png').convert()
    explosion_surface.set_colorkey((0,200,0))
    extra_bomb_surface = pygame.image.load('extra_bomb.png').convert()
    extra_bomb_surface.set_colorkey((0,200,0))
    longer_explosion_surface = pygame.image.load('longer_explosion.png').convert()
    longer_explosion_surface.set_colorkey((0,200,0))
    monster_surface = pygame.image.load('monster.png').convert()
    monster_surface.set_colorkey((0,200,0))
    pygame.display.set_caption('Bomberman')
    clock = pygame.time.Clock()
    # initialising objects
    player1 = player(50, 50, player1_surface, dead_surface1)
    player2 = player(675, 575, player2_surface, dead_surface2)
    players = []
    players.append(player1)
    players.append(player2)
    bombs = []
    explosions = []
    walls = []
    crumbly_walls = []
    powerups = []
    monsters = []
    game_lapse_time = 0
    fields = [[[] for i in range(15)] for j in range(13)]

    # Returns the list of game objects in Game.fields for a field based on coordinates.
    def get_objects_at_coords(x, y):
        row_index = y // 50
        column_index = x // 50
        return Game.fields[row_index][column_index]
    
    # Returns the list of game objects intersecting with an object.
    def get_objects_at_object(obj):
        potential_collisons = []
        for corner in [(obj.rect.topleft[0], obj.rect.topleft[1]), (obj.rect.topright[0], obj.rect.topright[1]), \
                       (obj.rect.bottomleft[0], obj.rect.bottomleft[1]), (obj.rect.bottomright[0], obj.rect.bottomright[1])]:
            for list_element in Game.get_objects_at_coords(corner[0], corner[1]):
                if list_element not in potential_collisons:
                    potential_collisons.append(list_element)
            
        return sum([potential_collisons], [])
    
    def field_has_bomb(x, y):
        for list_element in Game.get_objects_at_coords(x, y):
            if type(list_element) is bomb:
                print("BOMB HERE")
                return True
        print("NO BOMB HERE")
        return False

    # Spawning non-breakable walls
    def spawn_walls():
        wall_start_x = 0
        for x in range(15):
            wall_start_y = 0
            for y in range(13):
                if wall_start_x in [0, 700] or wall_start_y in [0, 600] or \
                    (wall_start_x in [100, 200, 300, 400, 500, 600] and wall_start_y in [100, 200, 300, 400, 500]):
                    wall_instance = wall(wall_start_x, wall_start_y)
                    Game.walls.append(wall_instance)
                    Game.fields[y][x].append(wall_instance)
                wall_start_y += 50
            wall_start_x += 50

    # Spawning breakable walls
    def spawn_crumbly_walls():
        forbidden_crumbly_wall_spots = [[50, 50], [50, 100], [100, 50], [650, 550], [600, 550], [650, 500]]
        crumbly_wall_start_x = 50
        for x in range(13):
            crumbly_wall_start_y = 50
            for y in range(11):
                if not (crumbly_wall_start_x in [100, 200, 300, 400, 500, 600] and crumbly_wall_start_y in [100, 200, 300, 400, 500]) and not \
                    [crumbly_wall_start_x, crumbly_wall_start_y] in forbidden_crumbly_wall_spots and random.randint(0,9) > 7:
                    crumbly_wall_instance = crumbly_wall(crumbly_wall_start_x, crumbly_wall_start_y)
                    Game.crumbly_walls.append(crumbly_wall_instance)
                    Game.fields[y+1][x+1].append(crumbly_wall_instance)
                crumbly_wall_start_y += 50
            crumbly_wall_start_x += 50

    # Tries moving the player if no collision occurs and collects pickups
    def move_or_collide(player_param, x, y):

        player_param.rect.x += x*(game_lapse_time/1000)
        player_param.rect.y += y*(game_lapse_time/1000)

        potential_collisons = Game.get_objects_at_object(player_param)

        for obj in potential_collisons:
            if type(obj) in [wall, crumbly_wall] and pygame.Rect.colliderect(player_param.rect, obj.rect):
                player_param.rect.x -= x*(game_lapse_time/1000)
                player_param.rect.y -= y*(game_lapse_time/1000)
            elif type(obj) is extra_bomb:
                player_param.max_bomb_count += 1
                Game.get_objects_at_coords(obj.rect.x, obj.rect.y).remove(obj)
                Game.powerups.remove(obj)
            elif type(obj) is longer_explosion:
                player_param.explosion_length += 1
                Game.get_objects_at_coords(obj.rect.x, obj.rect.y).remove(obj)
                potential_collisons.remove(obj)
                Game.powerups.remove(obj)

        for bomb_obj in Game.bombs:
            if not bomb_obj.stood_on and pygame.Rect.colliderect(player_param.rect, bomb_obj.rect): 
                player_param.rect.x -= 2*x
                player_param.rect.y -= 2*y

    # Pairs objects with textures
    def render_map():
        Game.screen.fill((0, 200, 0))

        for wall_obj in Game.walls:
            Game.screen.blit(Game.wall_surface, wall_obj)

        for crumbly_wall_obj in Game.crumbly_walls:
            Game.screen.blit(Game.crumbly_wall_surface, crumbly_wall_obj)
        
        for bomb_instance in Game.bombs:
            Game.screen.blit(Game.bomb_surface, bomb_instance)

        for explosion_instance in Game.explosions:
            Game.screen.blit(Game.explosion_surface, explosion_instance)

        for powerup_instance in Game.powerups:
            if type(powerup_instance) is extra_bomb:
                Game.screen.blit(Game.extra_bomb_surface, powerup_instance)
            elif type(powerup_instance) is longer_explosion:
                Game.screen.blit(Game.longer_explosion_surface, powerup_instance)

        for player in Game.players:
            if player.is_alive:
                Game.screen.blit(player.surface, player.rect)
            else:
                Game.screen.blit(player.dead_surface, player.rect)
        for monster_instance in Game.monsters:
            if monster_instance.is_alive:
                Game.screen.blit(Game.monster_surface, monster_instance.rect)
    # Moves player1 
    def move_player1():
        if Game.player1.is_alive:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] == True and Game.player1.bombs_deployed < Game.player1.max_bomb_count \
                and not Game.field_has_bomb(Game.player1.rect.x+10, Game.player1.rect.y+10):                
                bomb_instance = bomb((Game.player1.rect.x+10) - ((Game.player1.rect.x+10) % 50), 
                                     (Game.player1.rect.y+10) - ((Game.player1.rect.y+10) % 50), Game.player1)
                Game.bombs.append(bomb_instance)
                Game.get_objects_at_coords(Game.player1.rect.x+10, Game.player1.rect.y+10).append(bomb_instance)
                Game.player1.bombs_deployed += 1

            if key[pygame.K_a] == True:
                Game.move_or_collide(Game.player1, -300, 0)
            if key[pygame.K_d] == True:
                Game.move_or_collide(Game.player1, 300, 0)
            if key[pygame.K_w] == True:
                Game.move_or_collide(Game.player1, 0, -300)
            if key[pygame.K_s] == True:
                Game.move_or_collide(Game.player1, 0, 300)
            # Restricts player movement
            Game.player1.rect.clamp_ip(Game.screen.get_rect())

    # Moves player2
    def move_player2():
        if Game.player2.is_alive:
            key = pygame.key.get_pressed()
            if key[pygame.K_o] == True and Game.player2.bombs_deployed < Game.player2.max_bomb_count  \
                and not Game.field_has_bomb(Game.player2.rect.x+10, Game.player2.rect.y+10):
                bomb_instance = bomb((Game.player2.rect.x+10) - ((Game.player2.rect.x+10) % 50), 
                                     (Game.player2.rect.y+10) - ((Game.player2.rect.y+10) % 50), Game.player2)
                Game.bombs.append(bomb_instance)
                Game.get_objects_at_coords(Game.player2.rect.x+10, Game.player.rect.y+10).append(bomb_instance)
                Game.player2.bombs_deployed += 1

            if key[pygame.K_LEFT] == True:
                Game.move_or_collide(Game.player2, -300, 0)
            if key[pygame.K_RIGHT] == True:
                Game.move_or_collide(Game.player2, 300, 0)
            if key[pygame.K_UP] == True:
                Game.move_or_collide(Game.player2, 0, -300)
            if key[pygame.K_DOWN] == True:
                Game.move_or_collide(Game.player2, 0, 300)
            # Restricts player movement
            Game.player2.rect.clamp_ip(Game.screen.get_rect())

        
    def turn_monster_if_obstacle(monster_instance, collision_object):
        if pygame.Rect.colliderect(monster_instance.rect, collision_object.rect):
            monster_instance.rect.x -= monster_instance.x_direction
            monster_instance.rect.y -= monster_instance.y_direction
            if monster_instance.lapse > 150:
                monster_instance.change_direction_randomly()
                return True
            monster_instance.x_direction = monster_instance.x_direction*(-1)
            monster_instance.y_direction = monster_instance.y_direction*(-1)
            return True
        return False

    def move_monsters():
        for monster_instance in Game.monsters:
            if monster_instance.lapse == 0:
                monster_instance.change_direction_randomly()
                monster_instance.lapse = random.randint(400,1600)
            else:
                monster_instance.lapse -= 1
                monster_instance.rect.x += monster_instance.x_direction
                monster_instance.rect.y += monster_instance.y_direction

                potential_collisions = Game.get_objects_at_object(monster_instance)
                for obj in potential_collisions:
                    if type(obj) in [wall, crumbly_wall, bomb]:
                        if Game.turn_monster_if_obstacle(monster_instance, obj):
                            return
                for player in Game.players:
                    if pygame.Rect.colliderect(player.rect, monster_instance.rect):
                        player.player_died()
                
    def spawn_powerup(x, y):
        if random.randint(0,9) > 5:
            if random.randint(0,9) > 4:
                extrabomb_instance = extra_bomb(x, y)
                Game.powerups.append(extrabomb_instance)
                Game.get_objects_at_coords(x, y).append(extrabomb_instance)
                print(Game.get_objects_at_coords(x, y))
            else:
                longerexplosion_instance = longer_explosion(x, y)
                Game.powerups.append(longerexplosion_instance)
                Game.get_objects_at_coords(x, y).append(longerexplosion_instance)
                print(Game.get_objects_at_coords(x, y))

    def remove_destroyed_entities():
        for crumbly_wall_instance in Game.crumbly_walls:
            if crumbly_wall_instance.destroyed:
                Game.get_objects_at_coords(crumbly_wall_instance.rect.x, crumbly_wall_instance.rect.y).remove(crumbly_wall_instance)
                Game.crumbly_walls.remove(crumbly_wall_instance)
                Game.spawn_powerup(crumbly_wall_instance.rect.x, crumbly_wall_instance.rect.y)
        for monstery_instance in Game.monsters:
            if not monstery_instance.is_alive:
                Game.monsters.remove(monstery_instance)

    def handle_explosion():
        for explosion_instance in Game.explosions:
            if explosion_instance.lifetime > 0:
                explosion_instance.lifetime -= 1
            else:
                Game.explosions.remove(explosion_instance)
        for explosion_instance in Game.explosions:
            for player in Game.players:
                if pygame.Rect.colliderect(player.rect, explosion_instance.rect):
                    player.player_died()
            for monster_instance in Game.monsters:
                if pygame.Rect.colliderect(monster_instance.rect, explosion_instance.rect):
                    monster_instance.is_alive = False
            for bomb_instance in Game.bombs:
                if pygame.Rect.colliderect(explosion_instance.rect, bomb_instance.rect):
                    Game.explosions.append(explosion(explosion_instance.rect.x, explosion_instance.rect.y))
                    Game.explosions[-1].explode(bomb_instance.owner.explosion_length, Game)
                    Game.get_objects_at_coords(explosion_instance.rect.x, explosion_instance.rect.y).remove(bomb_instance)
                    Game.bombs.remove(bomb_instance)
                    bomb_instance.owner.bombs_deployed -= 1

    def handle_bombs():
        for bomb_instance in Game.bombs:
            if bomb_instance.fuse_time > 0:
                bomb_instance.fuse_time -= 1
            else:
                Game.explosions.append(explosion(bomb_instance.rect.x, bomb_instance.rect.y))
                Game.explosions[-1].explode(bomb_instance.owner.explosion_length, Game)
                Game.get_objects_at_coords(bomb_instance.rect.x, bomb_instance.rect.y).remove(bomb_instance)
                Game.bombs.remove(bomb_instance)
                bomb_instance.owner.bombs_deployed -= 1

    def spawn_monsters(count):
        forbidden_monster_spots = [[50, 50], [50, 100], [100, 50], [650, 550], [600, 550], [650, 500]]
        for i in range(count):
            can_spawn = False
            while not can_spawn:
                spawn_x = random.randint(1,13)*50
                spawn_y = random.randint(1,11)*50
                spawn_x += random.randint(0,24)
                spawn_y += random.randint(0,24)
                if [spawn_x, spawn_y] in forbidden_monster_spots:
                    continue
                can_spawn = True
                for crumbly_wall_instance in Game.crumbly_walls:
                    if crumbly_wall_instance.rect.collidepoint(spawn_x, spawn_y):
                        can_spawn = False
                for wall_instance in Game.walls:
                    if wall_instance.rect.collidepoint(spawn_x, spawn_y):
                        can_spawn = False
            Game.monsters.append(monster(spawn_x, spawn_y))

    def update_bomb_trampling(): 
        for bomb_instance in Game.bombs:
            bomb_instance.stood_on = False
            if pygame.Rect.colliderect(Game.player1.rect, bomb_instance.rect):
                bomb_instance.stood_on = True
            elif pygame.Rect.colliderect(Game.player2.rect, bomb_instance.rect):
                bomb_instance.stood_on = True
        return
    
    def tick_explosion():
        print(explosion.delay)
        if explosion.delay > 0:
            explosion.delay -= 1
        else:
            explosion.delay = 50


# Spawning walls and crumbly walls
Game.spawn_walls()
Game.spawn_crumbly_walls()
Game.spawn_monsters(1)
# Main loop
run = True
while run:
    # Shutting down if the player clicks on close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    Game.render_map()
    Game.update_bomb_trampling()
    Game.move_monsters()
    Game.move_player1()
    Game.move_player2()
    Game.handle_explosion()
    Game.handle_bombs()
    Game.remove_destroyed_entities()
    Game.tick_explosion()
    # Updating display and looping game at rate of 150 FPS
    pygame.display.update()
    Game.clock.tick(150)
    game_lapse_time = Game.clock.get_time()
pygame.quit()