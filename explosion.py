import pygame

class explosion:
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 50, 50))
        self.lifetime = 100

    def explode_branch(self, direction, offset, times, explosions, walls, crumbly_walls, monsters, player):
        if times > 0:

            if direction == "UP":
                explosions.append(explosion(self.rect.x, self.rect.y-offset))
            elif direction == "DOWN":
                explosions.append(explosion(self.rect.x, self.rect.y+offset))
            elif direction == "LEFT":
                explosions.append(explosion(self.rect.x-offset, self.rect.y))
            elif direction == "RIGHT":
                explosions.append(explosion(self.rect.x+offset, self.rect.y))
            for wall_instance in walls:
                if pygame.Rect.colliderect(wall_instance.rect, explosions[-1].rect):
                    explosions.remove(explosions[-1])
                    return
            for crumbly_wall_instance in crumbly_walls:
                if pygame.Rect.colliderect(crumbly_wall_instance.rect, explosions[-1].rect):
                    crumbly_wall_instance.destroyed = True
                    times = 0
            for monster_instance in monsters:
                if pygame.Rect.colliderect(monster_instance.rect, explosions[-1].rect):
                    monster_instance.is_alive = False
            if pygame.Rect.colliderect(player.rect, explosions[-1].rect):
                player.player_died()
            self.explode_branch(direction, offset+50, times-1, explosions, walls, crumbly_walls, monsters, player)

    def explode(self, times, explosions, walls, crumbly_walls, monsters, player):
        self.explode_branch("UP", 50, times, explosions, walls, crumbly_walls, monsters, player)
        self.explode_branch("DOWN", 50, times, explosions, walls, crumbly_walls, monsters, player)
        self.explode_branch("LEFT", 50, times, explosions, walls, crumbly_walls, monsters, player)
        self.explode_branch("RIGHT", 50, times, explosions, walls, crumbly_walls, monsters, player)
