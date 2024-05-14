import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *

class TestBarricadeClass(unittest.TestCase):
    pygame.init()
    pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))

    def test_get_bonus(self):
        barricade_instance = Barricade((0,0), 50)
        self.assertEqual(barricade_instance.get_bonus(), ("barricade", 3))

if __name__ == '__main__':
    unittest.main()