import pygame
import random

from wall import wall
from crumbly_wall import crumbly_wall
from bomb import bomb


pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 650

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
crumbly_wall_surface = pygame.image.load('crumbly_wall.png').convert()
wall_surface = pygame.image.load('wall.png').convert()
player_surface = pygame.image.load('player1.png').convert()
bomb_surface = pygame.image.load('bomb.png').convert()

pygame.display.set_caption('Bomberman')
clock = pygame.time.Clock()

player = pygame.Rect((50, 50, 25, 25))
bombs = []
bomb_cooldown = 0
walls = []
wall_start_x = 0
wall_start_y = 0

for x in range(15):
    wall_start_y = 0
    for y in range(13):
        if wall_start_x in [0, 700] or wall_start_y in [0, 600] or (wall_start_x in [100, 200, 300, 400, 500, 600] and wall_start_y in [100, 200, 300, 400, 500]):
            wall_instance = wall(wall_start_x, wall_start_y)
            print("Wall " + str(wall_instance.rect.x) + " " + str(wall_instance.rect.y))
            walls.append(wall_instance)
        wall_start_y += 50
    wall_start_x += 50

crumbly_walls = []
forbidden_crumbly_wall_spots = [[50, 50], [50, 100], [100, 50]]
crumbly_wall_start_x = 50
for x in range(13):
    crumbly_wall_start_y = 50
    for y in range(11):
        if not (crumbly_wall_start_x in [100, 200, 300, 400, 500, 600] and crumbly_wall_start_y in [100, 200, 300, 400, 500]) and not \
            [crumbly_wall_start_x, crumbly_wall_start_y] in forbidden_crumbly_wall_spots and random.randint(0,9) > 7:
            crumbly_wall_instance = crumbly_wall(crumbly_wall_start_x, crumbly_wall_start_y)
            print("Crumbly wall " + str(crumbly_wall_instance.rect.x) + " " + str(crumbly_wall_instance.rect.y))
            crumbly_walls.append(crumbly_wall_instance)
        crumbly_wall_start_y += 50
    crumbly_wall_start_x += 50

def move_or_collide(player_param, x, y):

    player_param.x += x
    player_param.y += y

    for wall_obj in walls:
        if pygame.Rect.colliderect(player_param, wall_obj):
            player_param.x -= x
            player_param.y -= y
            return
    for crumbly_wall_obj in crumbly_walls:
        if pygame.Rect.colliderect(player_param, crumbly_wall_obj):
            player_param.x -= x
            player_param.y -= y
            return
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

run = True
while run:

    screen.fill((0, 200, 0))

    for wall_obj in walls:
        screen.blit(wall_surface, wall_obj)

    for crumbly_wall_obj in crumbly_walls:
        screen.blit(crumbly_wall_surface, crumbly_wall_obj)
    
    for bomb_instance in bombs:
        screen.blit(bomb_surface, bomb_instance)

    screen.blit(player_surface, player)
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE] == True and bomb_cooldown == 0:
        bombs.append(bomb(player.x - (player.x % 50), player.y - (player.y % 50)))
        bomb_cooldown = 500

    if key[pygame.K_a] == True:
        move_or_collide(player, -1, 0)
    if key[pygame.K_d] == True:
        move_or_collide(player, 1, 0)
    if key[pygame.K_w] == True:
        move_or_collide(player, 0, -1)
    if key[pygame.K_s] == True:
        move_or_collide(player, 0, 1)


    player.clamp_ip(screen.get_rect())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if bomb_cooldown > 0:
       bomb_cooldown -= 1
    pygame.display.update()
    clock.tick(300)

pygame.quit()