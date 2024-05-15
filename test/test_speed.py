import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *

class TestSpeedClass(unittest.TestCase):
    pygame.init()
    pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))

    def test_get_bonus(self):
        speed_instance = Speed((0,0), 50)
        self.assertEqual(speed_instance.get_bonus(), ("speed", 1))

if __name__ == '__main__':
    unittest.main()