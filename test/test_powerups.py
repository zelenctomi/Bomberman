
import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *
from monster import *
from player import *

class TestPowerupsClass(unittest.TestCase):

    pygame.init()
    pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))

    def test_get_powerup(self):
        drop = Powerups.get_powerup((0, 0), 50)
        self.assertTrue(type(drop) in [Longer_explosion, Extra_bomb, type(None)])
    
if __name__ == '__main__':
    unittest.main()


