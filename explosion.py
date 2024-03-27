import pygame


class Explosion:
  def __init__(self, x: int, y: int, walls: list[pygame.Rect]):
    self.rect: pygame.Rect = pygame.Rect((x, y, 50, 50))
    self.lifetime: int = 100
    self.walls: list[pygame.Rect] = walls

  def spread(self, direction: str, offset: int, times: int): # Typehint -> list[Explosion] doesn't work due to recursion
    explosions: list[Explosion] = []
    if times > 0:
      if direction == "UP":
        explosions.append(Explosion(self.rect.x, self.rect.y - offset, self.walls))
      elif direction == "DOWN":
        explosions.append(Explosion(self.rect.x, self.rect.y + offset, self.walls))
      elif direction == "LEFT":
        explosions.append(Explosion(self.rect.x - offset, self.rect.y, self.walls))
      elif direction == "RIGHT":
        explosions.append(Explosion(self.rect.x + offset, self.rect.y, self.walls))
      for wall in self.walls:
        if pygame.Rect.colliderect(wall, explosions[-1].rect):
          explosions.pop()
          return explosions
      return explosions + self.spread(direction, offset + 50, times - 1)
    return []

  def initiate(self, times: int): # Typehint -> list[Explosion] doesn't work due to recursion
    return [Explosion(self.rect.x, self.rect.y, self.walls)]  \
            + self.spread("UP", 50, times)                    \
            + self.spread("DOWN", 50, times)                  \
            + self.spread("LEFT", 50, times)                  \
            + self.spread("RIGHT", 50, times)
  
  def update(self) -> int:
    self.lifetime -= 1
    return self.lifetime
