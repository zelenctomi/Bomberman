import pygame

class explosion:
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 50, 50))
        self.lifetime = 100

    def explode_branch(self, direction, offset, times, explosions, bombs, walls, crumbly_walls):
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


            self.explode_branch(direction, offset+50, times-1, explosions, bombs, walls, crumbly_walls)

    def explode(self, times, explosions, bombs, walls, crumbly_walls):
        self.explode_branch("UP", 50, times, explosions, bombs, walls, crumbly_walls)
        self.explode_branch("DOWN", 50, times, explosions, bombs, walls, crumbly_walls)
        self.explode_branch("LEFT", 50, times, explosions, bombs, walls, crumbly_walls)
        self.explode_branch("RIGHT", 50, times, explosions, bombs, walls, crumbly_walls)
