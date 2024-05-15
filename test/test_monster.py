import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *
from monster import *

class TestMonsterClass(unittest.TestCase):
    pygame.init()
    pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))

    def test_die(self):
        test_fields: Fields = Fields()
        monster_instance = Monster((0,0), test_fields)
        monster_instance.load_assets()
        monster_instance.die()
        self.assertEqual(monster_instance.alive, False)
    
    def test_change_direction_1(self):
        test_fields: Fields = Fields()
        monster_instance = Monster((0,0), test_fields)
        monster_instance.load_assets()
        monster_instance.move()
        self.assertTrue(monster_instance.rect.x in [0, 1, -1])
    
    def test_change_direction_2(self):
        test_fields: Fields = Fields()
        monster_instance = Monster((0,0), test_fields)
        monster_instance.load_assets()
        monster_instance.move()
        self.assertTrue(monster_instance.rect.y in [0, 1, -1])

    def test_respawn_1(self):
        test_fields: Fields = Fields()
        monster_instance = Monster((0,0), test_fields)
        monster_instance.load_assets()
        monster_instance.respawn((1,1))
        self.assertTrue(monster_instance.rect.x == 1 and monster_instance.rect.y == 1)

    def test_respawn_2(self):
        test_fields: Fields = Fields()
        monster_instance = Monster((0,0), test_fields)
        monster_instance.load_assets()
        monster_instance.respawn((100,100))
        self.assertTrue(monster_instance.rect.x == 100 and monster_instance.rect.y == 100)

if __name__ == '__main__':
    unittest.main()