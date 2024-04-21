
import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *
from monster import *
from player import *

class TestFieldsClass(unittest.TestCase):


    pygame.init()
    pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))

    def test_get_crumbly_walls_1(self):
        test_fields: Fields = Fields()
        self.assertEqual(test_fields.get_crumbly_walls(), [])
    
    def test_get_crumbly_walls_2(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        test_fields.walls.append(crumbly_wall_instance)
        self.assertEqual(test_fields.get_crumbly_walls(), [crumbly_wall_instance])

    def test_get_objects_1(self):
        test_fields: Fields = Fields()
        self.assertEqual(test_fields.get_objects(0,0), [])

    def test_get_objects_2(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        test_fields.fields[0][0].append(crumbly_wall_instance)
        self.assertEqual(test_fields.get_objects(0,0), [crumbly_wall_instance])

    def test_get_objects_at_coords_1(self):
        test_fields: Fields = Fields()
        self.assertEqual(test_fields.get_objects_at_coords(0,0), [])

    def test_get_objects_at_coords_2(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        test_fields.fields[0][0].append(crumbly_wall_instance)
        self.assertEqual(test_fields.get_objects_at_coords(0,0), [crumbly_wall_instance])

    def test_get_objects_at_object_1(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        test_fields.fields[0][0].append(crumbly_wall_instance)
        self.assertEqual(test_fields.get_objects_at_object(crumbly_wall_instance), [crumbly_wall_instance])

    def test_get_objects_at_object_2(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        monster_instance = Monster((0,0), test_fields)
        monster_instance_2 = Monster((20,20), test_fields)
        test_fields.fields[0][0].append(monster_instance)
        test_fields.fields[0][0].append(monster_instance_2)
        self.assertEqual(test_fields.get_objects_at_object(crumbly_wall_instance), [monster_instance, monster_instance_2])

    '''
    def test_get_objects_around_object_1(self):
        test_fields: Fields = Fields()
        monster_instance = Monster((0,0), test_fields)
        test_fields.fields[0][0].append(monster_instance)
        self.assertEqual(test_fields.get_objects_at_object(monster_instance), [])

    def test_get_objects_around_object_2(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        monster_instance = Monster((0,0), test_fields)
        #test_fields.fields[0][0].append(crumbly_wall_instance)
        test_fields.fields[0][0].append(monster_instance)
        self.assertEqual(test_fields.get_objects_at_object(monster_instance), [crumbly_wall_instance])
    '''

    def test_snap_to_grid_1(self):
        test_fields: Fields = Fields()
        test_rect: pygame.Rect = pygame.Rect(10, 10, 50, 50)
        test_rect = test_fields.snap_to_grid(test_rect)
        self.assertEqual([test_rect.x, test_rect.y], [0, 0])

    def test_snap_to_grid_2(self):
        test_fields: Fields = Fields()
        test_rect: pygame.Rect = pygame.Rect(51, 51, 50, 50)
        test_rect = test_fields.snap_to_grid(test_rect)
        self.assertEqual([test_rect.x, test_rect.y], [50, 50])

    def test_field_has_bomb_1(self):
        test_fields: Fields = Fields()

        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        test_fields.fields[0][0].append(test_bomb)

        self.assertEqual(test_fields.field_has_bomb(0, 0), True)

    def test_field_has_bomb_2(self):
        test_fields: Fields = Fields()

        self.assertEqual(test_fields.field_has_bomb(0, 0), False)

    def test_set_bomb_1(self):
        test_fields: Fields = Fields()

        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        test_fields.set_bomb(0, 0, test_bomb)

        self.assertEqual(test_fields.bombs, [test_bomb])

    def test_set_bomb_2(self):
        test_fields: Fields = Fields()

        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb_1: Bomb = Bomb([0, 0], 50, test_player)
        test_bomb_2: Bomb = Bomb([50, 50], 50, test_player)
        test_fields.set_bomb(0, 0, test_bomb_1)
        test_fields.set_bomb(50, 50, test_bomb_2)

        self.assertEqual(test_fields.bombs, [test_bomb_1, test_bomb_2])

    def test_update_bombs_1(self):
        test_fields: Fields = Fields()

        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        test_bomb.timer = 0
        test_fields.bombs.append(test_bomb)
        test_fields.fields[0][0].append(test_bomb)
        test_fields.update_bombs()
        self.assertEqual(test_fields.bombs, [])

    def test_update_bombs_2(self):
        test_fields: Fields = Fields()

        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        test_fields.bombs.append(test_bomb)
        test_fields.fields[0][0].append(test_bomb)
        test_fields.update_bombs()
        self.assertEqual(test_fields.bombs, [test_bomb])

    def test_update_explosions_1(self):
        test_fields: Fields = Fields()
        test_explosion: Explosion = Explosion(0, 0, [Wall(50, 50)])
        test_explosion.lifetime = 1
        test_fields.explosions.append(test_explosion)
        test_fields.update_explosions()
        self.assertEqual(test_fields.explosions, [])
    
    def test_update_explosions_2(self):
        test_fields: Fields = Fields()
        test_explosion: Explosion = Explosion(0, 0, [Wall(50, 50)])
        test_explosion.lifetime = 2
        test_fields.explosions.append(test_explosion)
        test_fields.update_explosions()
        self.assertEqual(test_fields.explosions, [test_explosion])

if __name__ == '__main__':
    unittest.main()


