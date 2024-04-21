
import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *
from monster import *

class TestFieldsClass(unittest.TestCase):

    def test_get_crumbly_walls_1(self):
        test_fields: Fields = Fields()
        self.assertEqual(test_fields.get_crumbly_walls(), [])
    
    def test_get_crumbly_walls_2(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        test_fields.walls.append(crumbly_wall_instance)
        self.assertEqual(test_fields.get_crumbly_walls(), [crumbly_wall_instance])

    def test_get_objects_1(self):
        test_fields: Fields = Fields()
        self.assertEqual(test_fields.get_objects(0,0), [])

    def test_get_objects_2(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        test_fields.fields[0][0].append(crumbly_wall_instance)
        self.assertEqual(test_fields.get_objects(0,0), [crumbly_wall_instance])

    def test_get_objects_at_coords_1(self):
        test_fields: Fields = Fields()
        self.assertEqual(test_fields.get_objects_at_coords(0,0), [])

    def test_get_objects_at_coords_2(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        test_fields.fields[0][0].append(crumbly_wall_instance)
        self.assertEqual(test_fields.get_objects_at_coords(0,0), [crumbly_wall_instance])

    def test_get_objects_at_object_1(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        test_fields.fields[0][0].append(crumbly_wall_instance)
        self.assertEqual(test_fields.get_objects_at_object(crumbly_wall_instance), [crumbly_wall_instance])

    def test_get_objects_at_object_2(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        monster_instance = Monster((0,0), test_fields)
        monster_instance_2 = Monster((20,20), test_fields)
        test_fields.fields[0][0].append(monster_instance)
        test_fields.fields[0][0].append(monster_instance_2)
        self.assertEqual(test_fields.get_objects_at_object(crumbly_wall_instance), [monster_instance, monster_instance_2])
'''
    def test_get_objects_around_object_1(self):
        test_fields: Fields = Fields()
        monster_instance = Monster((0,0), test_fields)
        test_fields.fields[0][0].append(monster_instance)
        self.assertEqual(test_fields.get_objects_at_object(monster_instance), [])

    def test_get_objects_around_object_2(self):
        test_fields: Fields = Fields()
        crumbly_wall_instance = Crumbly_wall(0,0)
        monster_instance = Monster((0,0), test_fields)
        #test_fields.fields[0][0].append(crumbly_wall_instance)
        test_fields.fields[0][0].append(monster_instance)
        self.assertEqual(test_fields.get_objects_at_object(monster_instance), [crumbly_wall_instance])
'''
if __name__ == '__main__':
    unittest.main()


