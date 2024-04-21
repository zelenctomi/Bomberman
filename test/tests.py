'''
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *

# This is the function you want to test
def add(a, b):
    return a + b

# This is your test case class
class TestAddFunction(unittest.TestCase):
    def test_add(self):
        # Test if 1 + 1 equals 2
        self.assertEqual(add(1, 1), 2)

        # Test if -1 + 1 equals 0
        self.assertEqual(add(-1, 1), 0)

    #def spawnTest(self):
    #    test_fields: Fields = Fields()
    #    test_spawner: Spawner = Spawner(test_fields)
    #    test_players: list[Player] = test_spawner.spawn_players([Settings.P1_CONTROLS, Settings.P2_CONTROLS, Settings.P3_CONTROLS])

    def fields_test_get_crumbly_walls(self):
        test_fields: Fields = Fields()
        self.assertEqual(test_fields.get_crumbly_walls(), [])

# This allows the test to be run
if __name__ == '__main__':
    unittest.main()
'''