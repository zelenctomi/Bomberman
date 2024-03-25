from fields import *


class Player:
  def __init__(self, x: int, y: int, fields: Fields, controls: dict[str, pygame.key.key_code]):
    self.rect: pygame.Rect = pygame.Rect((x, y, 25, 25))
    self.controls: dict[str, pygame.key.key_code] = controls
    self.fields: Fields = fields
    self.bomb: (Bomb | None) = None
    self.is_alive: bool = True
    # Stats #
    self.stats: dict[str, int] = {
      'bomb': 2,
      'explosion': 2
    }

  def draw(self, surface: pygame.Surface, dead_surface: pygame.Surface) -> None:
    self.surface: pygame.Surface = surface
    self.dead_surface: pygame.Surface = dead_surface

  def die(self) -> None:
    self.is_alive = False

  def move(self, screen: pygame.Surface, elapsed: int) -> None:
    if self.is_alive:
      key: list[bool] = pygame.key.get_pressed()
      if key[self.controls['place']] and self.stats['bomb'] > 0 \
              and not self.fields.field_has_bomb(self.rect.x + 10, self.rect.y + 10):
        self.place_bomb(self.rect.x, self.rect.y)
      if key[self.controls['left']]:
        self.move_or_collide(-300, 0, elapsed)
      if key[self.controls['right']]:
        self.move_or_collide(300, 0, elapsed)
      if key[self.controls['up']]:
        self.move_or_collide(0, -300, elapsed)
      if key[self.controls['down']]:
        self.move_or_collide(0, 300, elapsed)
      self.rect.clamp_ip(screen.get_rect())

  def move_or_collide(self, x: int, y: int, elapsed: int) -> None:
    self.rect.x += x * (elapsed / 1000)
    self.rect.y += y * (elapsed / 1000)
    potential_collisons: list[pygame.Rect] = self.fields.get_objects_at_object(self)
    if self.bomb != None and self.bomb not in potential_collisons:
      self.bomb = None

    for obj in potential_collisons:
      if isinstance(obj, (Wall, Bomb)) and obj != self.bomb and pygame.Rect.colliderect(self.rect, obj.rect):
          self.rect.x -= x * (elapsed / 1000)
          self.rect.y -= y * (elapsed / 1000)
      elif isinstance(obj, Powerup):
        self.apply_powerup(obj)
        self.fields.get_objects_at_coords(obj.rect.x, obj.rect.y).remove(obj)
        self.fields.powerups.remove(obj)

  def apply_powerup(self, powerup: Powerup) -> None:
    stat: str
    value: int
    stat, value = powerup.get_bonus()
    self.stats[stat] += value

  def place_bomb(self, x: int, y: int) -> None:
    bomb: Bomb = Bomb((x + 10) - ((x + 10) % 50), (y + 10) - ((y + 10) % 50), self)
    self.fields.set_bomb(x, y, bomb)
    self.stats['bomb'] -= 1
    self.bomb = bomb
