
import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *
from monster import *
from player import *

class TestExplosionClass(unittest.TestCase):

    pygame.init()
    pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))

    def test_spread_1(self):
        wall_instance = Wall(0,0)
        test_explosion = Explosion(0, 0, [wall_instance])
        test_explosion_collection = test_explosion.spread("UP", 50, 1)                    

        self.assertEqual(len(test_explosion_collection), 1)

    def test_spread_2(self):
        wall_instance = Wall(0,0)
        test_explosion = Explosion(0, 0, [wall_instance])
        test_explosion_collection = test_explosion.spread("UP", 50, 2)                    

        self.assertEqual(len(test_explosion_collection), 2)

    #Explosion spread blocked
    def test_spread_3(self):
        wall_instance = Wall(50,0)
        test_explosion = Explosion(50, 50, [wall_instance])
        test_explosion_collection = test_explosion.spread("UP", 50, 2)                    

        self.assertEqual(len(test_explosion_collection), 0)

    #Explosion spread not blocked
    def test_spread_4(self):
        wall_instance = Wall(0,0)
        test_explosion = Explosion(50, 50, [wall_instance])
        test_explosion_collection = test_explosion.spread("UP", 50, 2)                    

        self.assertEqual(len(test_explosion_collection), 2)

    def test_initiate_1(self):
        wall_instance = Wall(0,0)
        test_explosion = Explosion(50, 50, [wall_instance])
        test_explosion_collection = test_explosion.initiate(1)                    

        self.assertEqual(len(test_explosion_collection), 5)

    def test_initiate_2(self):
        wall_instance = Wall(0,0)
        test_explosion = Explosion(50, 50, [wall_instance])
        test_explosion_collection = test_explosion.initiate(2)                    

        self.assertEqual(len(test_explosion_collection), 9)

    def test_initiate_3(self):
        wall_instance = Wall(0,0)
        test_explosion = Explosion(50, 50, [wall_instance])
        test_explosion_collection = test_explosion.initiate(3)                    

        self.assertEqual(len(test_explosion_collection), 13)

    def test_update_1(self):
        wall_instance = Wall(0,0)
        test_explosion = Explosion(50, 50, [wall_instance])
        test_explosion.update()
        self.assertEqual(test_explosion.lifetime, 99)

    def test_update_2(self):
        wall_instance = Wall(0,0)
        test_explosion = Explosion(50, 50, [wall_instance])
        test_explosion.update()
        test_explosion.update()
        test_explosion.update()
        self.assertEqual(test_explosion.lifetime, 97)
    
if __name__ == '__main__':
    unittest.main()


