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

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 650

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
crumbly_wall_surface = pygame.image.load('crumbly_wall.png').convert()
wall_surface = pygame.image.load('wall.png').convert()
bomb_surface = pygame.image.load('bomb.png').convert()
explosion_surface = pygame.image.load('explosion_center.png').convert()
extra_bomb_surface = pygame.image.load('extra_bomb.png').convert()
longer_explosion_surface = pygame.image.load('longer_explosion.png').convert()
monster_surface = pygame.image.load('monster.png').convert()

pygame.display.set_caption('Bomberman')
clock = pygame.time.Clock()

player1 = player(50, 50)
bombs = []
explosions = []
walls = []
crumbly_walls = []
powerups = []
monsters = []

def spawn_walls():
    wall_start_x = 0
    for x in range(15):
        wall_start_y = 0
        for y in range(13):
            if wall_start_x in [0, 700] or wall_start_y in [0, 600] or \
                (wall_start_x in [100, 200, 300, 400, 500, 600] and wall_start_y in [100, 200, 300, 400, 500]):
                wall_instance = wall(wall_start_x, wall_start_y)
                walls.append(wall_instance)
            wall_start_y += 50
        wall_start_x += 50

def spawn_crumbly_walls():
    forbidden_crumbly_wall_spots = [[50, 50], [50, 100], [100, 50]]
    crumbly_wall_start_x = 50
    for x in range(13):
        crumbly_wall_start_y = 50
        for y in range(11):
            if not (crumbly_wall_start_x in [100, 200, 300, 400, 500, 600] and crumbly_wall_start_y in [100, 200, 300, 400, 500]) and not \
                [crumbly_wall_start_x, crumbly_wall_start_y] in forbidden_crumbly_wall_spots and random.randint(0,9) > 7:
                crumbly_wall_instance = crumbly_wall(crumbly_wall_start_x, crumbly_wall_start_y)
                crumbly_walls.append(crumbly_wall_instance)
            crumbly_wall_start_y += 50
        crumbly_wall_start_x += 50

def move_or_collide(player_param, x, y):

    player_param.rect.x += 2*x
    player_param.rect.y += 2*y

    for wall_obj in walls:
        if pygame.Rect.colliderect(player_param.rect, wall_obj.rect):
            player_param.rect.x -= 2*x
            player_param.rect.y -= 2*y
    for crumbly_wall_obj in crumbly_walls:
        if pygame.Rect.colliderect(player_param.rect, crumbly_wall_obj.rect):
            player_param.rect.x -= 2*x
            player_param.rect.y -= 2*y
    for powerup_instance in powerups:
        if pygame.Rect.colliderect(player_param.rect, powerup_instance.rect):
            if type(powerup_instance) is extra_bomb:
                player_param.max_bomb_count += 1
            elif type(powerup_instance) is longer_explosion:
                player_param.explosion_length += 1
            powerups.remove(powerup_instance)
'''
        
    for bomb_obj in bombs:
        if pygame.Rect.collidepoint(player_param.center, bomb_obj): 
            player_param.x -= x
            player_param.y -= y
            return
    for bomb_obj in bombs:
        if pygame.Rect.colliderect(player_param, bomb_obj) and \
            ((((player_param.x - (player_param.x % 50)) != ((player_param.x-x) - ((player_param.x-x) % 50))) or 
             ((player_param.y - (player_param.y % 50)) != ((player_param.y-y) - ((player_param.y-y) % 50)))) or
            (((player_param.bottomright[0] - (player_param.bottomright[0] % 50)) != ((player_param.bottomright[0]-x) - ((player_param.bottomright[0]-x) % 50))) or 
             ((player_param.bottomright[1] - (player_param.bottomright[1] % 50)) != ((player_param.bottomright[1]-y) - ((player_param.bottomright[1]-y) % 50))))):
            player_param.x -= x
            player_param.y -= y
            return
'''

def render_map():
    screen.fill((0, 200, 0))

    for wall_obj in walls:
        screen.blit(wall_surface, wall_obj)

    for crumbly_wall_obj in crumbly_walls:
        screen.blit(crumbly_wall_surface, crumbly_wall_obj)
    
    for bomb_instance in bombs:
        screen.blit(bomb_surface, bomb_instance)

    for explosion_instance in explosions:
        screen.blit(explosion_surface, explosion_instance)

    for powerup_instance in powerups:
        if type(powerup_instance) is extra_bomb:
            screen.blit(extra_bomb_surface, powerup_instance)
        elif type(powerup_instance) is longer_explosion:
            screen.blit(longer_explosion_surface, powerup_instance)

    screen.blit(player1.player_surface, player1.rect)
    for monster_instance in monsters:
        screen.blit(monster_surface, monster_instance.rect)


def move_players():
    if player1.is_alive:
        key = pygame.key.get_pressed()
        standing_on_bomb = False
        for bomb_instance in bombs:
            if pygame.Rect.colliderect(player1.rect, bomb_instance.rect):
                standing_on_bomb = True
        if key[pygame.K_SPACE] == True and player1.bombs_deployed < player1.max_bomb_count and not standing_on_bomb:
            bombs.append(bomb((player1.rect.x+10) - ((player1.rect.x+10) % 50), (player1.rect.y+10) - ((player1.rect.y+10) % 50), player1))
            player1.bombs_deployed += 1

        if key[pygame.K_a] == True:
            move_or_collide(player1, -1, 0)
        if key[pygame.K_d] == True:
            move_or_collide(player1, 1, 0)
        if key[pygame.K_w] == True:
            move_or_collide(player1, 0, -1)
        if key[pygame.K_s] == True:
            move_or_collide(player1, 0, 1)

        player1.rect.clamp_ip(screen.get_rect())

def move_monsters():
    for monster_instance in monsters:
        if monster_instance.lapse == 0:
            monster_instance.change_direction_randomly()
            monster_instance.lapse = random.randint(400,1600)
        else:
            monster_instance.lapse -= 1
            monster_instance.rect.x += monster_instance.x_direction
            monster_instance.rect.y += monster_instance.y_direction

            for wall_obj in walls:
                if pygame.Rect.colliderect(monster_instance.rect, wall_obj.rect):
                    monster_instance.rect.x -= monster_instance.x_direction
                    monster_instance.rect.y -= monster_instance.y_direction
                    if monster_instance.lapse > 150:
                        monster_instance.change_direction_randomly()
                        return
                    monster_instance.x_direction = monster_instance.x_direction*(-1)
                    monster_instance.y_direction = monster_instance.y_direction*(-1)
                    return
            for crumbly_wall_obj in crumbly_walls:
                if pygame.Rect.colliderect(monster_instance.rect, crumbly_wall_obj.rect):
                    monster_instance.rect.x -= monster_instance.x_direction
                    monster_instance.rect.y -= monster_instance.y_direction
                    if monster_instance.lapse > 150:
                        monster_instance.change_direction_randomly()
                        return
                    monster_instance.x_direction = monster_instance.x_direction*(-1)
                    monster_instance.y_direction = monster_instance.y_direction*(-1)
                    return
            if pygame.Rect.colliderect(monster_instance.rect, player1.rect):
                player1.player_died()
                    
            
def spawn_powerup(x, y):
    if random.randint(0,9) > 5:
        if random.randint(0,9) > 4:
            powerups.append(extra_bomb(x, y))
        else:
            powerups.append(longer_explosion(x, y))

def remove_destroyed_entities():
    for crumbly_wall_instance in crumbly_walls:
        if crumbly_wall_instance.destroyed:
            crumbly_walls.remove(crumbly_wall_instance)
            spawn_powerup(crumbly_wall_instance.rect.x, crumbly_wall_instance.rect.y)
    for monstery_instance in monsters:
        if not monstery_instance.is_alive:
            monsters.remove(monstery_instance)

def handle_explosion():
    for explosion_instance in explosions:
        if explosion_instance.lifetime > 0:
            explosion_instance.lifetime -= 1
        else:
            explosions.remove(explosion_instance)

def handle_bombs():
    for bomb_instance in bombs:
        if bomb_instance.fuse_time > 0:
            bomb_instance.fuse_time -= 1
        else:
            explosions.append(explosion(bomb_instance.rect.x, bomb_instance.rect.y))
            explosions[-1].explode(player1.explosion_length, explosions, walls, crumbly_walls, monsters, player1)
            bombs.remove(bomb_instance)
            bomb_instance.owner.bombs_deployed -= 1

def spawn_monsters(count):
    for i in range(count):
        can_spawn = False
        spawn_x = random.randint(1,13)*50
        spawn_y = random.randint(1,11)*50
        while not can_spawn:
            spawn_x = random.randint(1,13)*50
            spawn_y = random.randint(1,11)*50
            can_spawn = True
            for crumbly_wall_instance in crumbly_walls:
                if crumbly_wall_instance.rect.collidepoint(spawn_x, spawn_y):
                    can_spawn = False
            for wall_instance in walls:
                if wall_instance.rect.collidepoint(spawn_x, spawn_y):
                    can_spawn = False
        monsters.append(monster(spawn_x, spawn_y))
    
        
    



# Spawning walls and crumbly walls
spawn_walls()
spawn_crumbly_walls()
spawn_monsters(10)
# Main loop
run = True
while run:
    # Shutting down if the player clicks on close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    render_map()
    move_monsters()
    move_players()
    handle_explosion()
    handle_bombs()
    remove_destroyed_entities()
    # Updating display and looping game at rate of 300 FPS
    pygame.display.update()
    clock.tick(150)
pygame.quit()