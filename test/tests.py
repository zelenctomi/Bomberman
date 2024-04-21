
import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_fields_test_get_crumbly_walls(self):
        test_fields: Fields = Fields()
        self.assertEqual(test_fields.get_crumbly_walls(), [])

if __name__ == '__main__':
    unittest.main()


