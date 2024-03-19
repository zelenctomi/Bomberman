import pygame

class Explosion:
	delay = 50
	def __init__(self, x, y):
			self.rect = pygame.Rect((x, y, 50, 50))
			self.lifetime = 100

	def explode_branch(self, direction, offset, times, game):
		if times > 0:
			if direction == "UP":
					game.explosions.append(Explosion(self.rect.x, self.rect.y-offset))
			elif direction == "DOWN":
					game.explosions.append(Explosion(self.rect.x, self.rect.y+offset))
			elif direction == "LEFT":
					game.explosions.append(Explosion(self.rect.x-offset, self.rect.y))
			elif direction == "RIGHT":
					game.explosions.append(Explosion(self.rect.x+offset, self.rect.y))
			for wall_instance in game.walls:
					if pygame.Rect.colliderect(wall_instance.rect, game.explosions[-1].rect):
							game.explosions.remove(game.explosions[-1])
							return
			for crumbly_wall_instance in game.crumbly_walls:
					if pygame.Rect.colliderect(crumbly_wall_instance.rect, game.explosions[-1].rect):
							crumbly_wall_instance.destroyed = True
							return

			self.explode_branch(direction, offset+50, times-1, game)

	def explode(self, times, game):
		self.explode_branch("UP", 50, times, game)
		self.explode_branch("DOWN", 50, times, game)
		self.explode_branch("LEFT", 50, times, game)
		self.explode_branch("RIGHT", 50, times, game)
