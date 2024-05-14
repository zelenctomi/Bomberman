
import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# test comment
from fields import *
from monster import *
from player import *

class TestBombClass(unittest.TestCase):

    pygame.init()
    pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))

    def test_update_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_bomb: Bomb = Bomb((0, 0), 50, test_player)
        test_bomb.update()
        test_bomb.update()
        test_bomb.update()
        self.assertEqual(test_bomb.timer, 180)

    def test_explode_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_bomb: Bomb = Bomb((0, 0), 50, test_player)
        wall_instance = Wall((0,0), 50)
        #crumbly_wall_instance = Crumbly_wall((0,0), 50)
        self.assertEqual(len(test_bomb.explode([wall_instance.rect],[])), 9)

    def test_update_frame_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_bomb: Bomb = Bomb((0, 0), 50, test_player)
        test_bomb.update_frame()
        self.assertEqual(test_bomb.frame, 0)

    def test_update_frame_2(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_bomb: Bomb = Bomb((0, 0), 50, test_player)
        test_bomb.update_frame()
        test_bomb.update_frame()
        self.assertEqual(test_bomb.frame, 0)

    def test_update_surface(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_bomb: Bomb = Bomb((0, 0), 50, test_player)
        self.assertEqual(test_bomb.surface, test_player.bomb_frame)
        
if __name__ == '__main__':
    unittest.main()


