import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *

class TestExtraBombClass(unittest.TestCase):
    pygame.init()
    pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))

    def test_get_bonus(self):
        extra_bomb_instance = Extra_bomb((0,0), 50)
        self.assertEqual(extra_bomb_instance.get_bonus(), ("bomb", 1))

if __name__ == '__main__':
    unittest.main()