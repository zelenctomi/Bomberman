
import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *
from monster import *
from player import *

class TestBombClass(unittest.TestCase):

    pygame.init()
    pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))

    def test_update_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        test_bomb.update()
        self.assertEqual(test_bomb.timer, 179)

    def test_update_2(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        test_bomb.update()
        test_bomb.update()
        self.assertEqual(test_bomb.timer, 178)

    def test_explode_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        wall_instance = Wall(0,0)
        self.assertEqual(len(test_bomb.explode([wall_instance])), 9)

    def test_update_frame_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        test_bomb.update_frame()
        self.assertEqual(test_bomb.frame, 1)

    def test_update_frame_2(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        test_bomb.update_frame()
        test_bomb.update_frame()
        self.assertEqual(test_bomb.frame, 2)

    def test_update_surface_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        test_surface = pygame.image.load('Assets/Walls/Default/wall.png').convert_alpha()
        test_bomb.update_surface(test_surface)
        self.assertEqual(test_bomb.surface, test_surface)

    def test_update_surface_2(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_bomb: Bomb = Bomb([0, 0], 50, test_player)
        self.assertEqual(test_bomb.surface, test_player.bomb_frame)

if __name__ == '__main__':
    unittest.main()


