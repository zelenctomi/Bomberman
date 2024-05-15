import pygame
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fields import *
from player import *
from unittest.mock import patch

class TestPlayerClass(unittest.TestCase):
    pygame.init()
    pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))

    def test_die_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.die()
        self.assertEqual(test_player.alive, False)

    def test_die_2(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.stats['invulnerability'] = 1
        test_player.die()
        self.assertEqual(test_player.alive, True)

    def test_update_frame_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.update_frame()
        self.assertEqual(test_player.frame, 1)

    def test_update_frame_2(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.update_frame()
        test_player.update_frame()
        self.assertEqual(test_player.frame, 2)

    def test_move_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        #pygame.key.get_pressed = lambda: {test_player.controls['left']: True}
        test_player.move()

        initial_x = test_player.rect.x
        initial_y = test_player.rect.y
        self.assertTrue(test_player.rect.x == initial_x and test_player.rect.y == initial_y)

    @patch('pygame.key.get_pressed')
    def test_move_2(self, mock_get_pressed):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        # Simulate a left key press
        mock_get_pressed.return_value = {test_player.controls['left']: True, 
                                        test_player.controls['place']: False,
                                        test_player.controls['barricade']: False,
                                        test_player.controls['right']: False,
                                        test_player.controls['up']: False,
                                        test_player.controls['down']: False}

        initial_x = test_player.rect.x
        initial_y = test_player.rect.y

        test_player.move()

        self.assertEqual(test_player.rect.x, initial_x - 1)
        self.assertEqual(test_player.rect.y, initial_y)

    @patch('pygame.key.get_pressed')
    def test_move_3(self, mock_get_pressed):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        # Simulate a left key press
        mock_get_pressed.return_value = {test_player.controls['left']: False, 
                                        test_player.controls['place']: False,
                                        test_player.controls['barricade']: False,
                                        test_player.controls['right']: True,
                                        test_player.controls['up']: False,
                                        test_player.controls['down']: False}

        initial_x = test_player.rect.x
        initial_y = test_player.rect.y

        test_player.move()

        self.assertEqual(test_player.rect.x, initial_x + 1)
        self.assertEqual(test_player.rect.y, initial_y)

    @patch('pygame.key.get_pressed')
    def test_move_4(self, mock_get_pressed):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        # Simulate a left key press
        mock_get_pressed.return_value = {test_player.controls['left']: False, 
                                        test_player.controls['place']: False,
                                        test_player.controls['barricade']: False,
                                        test_player.controls['right']: False,
                                        test_player.controls['up']: True,
                                        test_player.controls['down']: False}

        initial_x = test_player.rect.x
        initial_y = test_player.rect.y

        test_player.move()

        self.assertEqual(test_player.rect.x, initial_x)
        self.assertEqual(test_player.rect.y, initial_y - 1)

    @patch('pygame.key.get_pressed')
    def test_move_5(self, mock_get_pressed):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        # Simulate a left key press
        mock_get_pressed.return_value = {test_player.controls['left']: False, 
                                        test_player.controls['place']: False,
                                        test_player.controls['barricade']: False,
                                        test_player.controls['right']: False,
                                        test_player.controls['up']: False,
                                        test_player.controls['down']: True}

        initial_x = test_player.rect.x
        initial_y = test_player.rect.y

        test_player.move()

        self.assertEqual(test_player.rect.x, initial_x)
        self.assertEqual(test_player.rect.y, initial_y + 1)

    def test_check_extra_powerups_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.stats['invulnerability'] = 1
        test_player.check_extra_powerups()

        self.assertEqual(test_player.invulnerability_timer, 719)
    
    def test_check_extra_powerups_2(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.stats['invulnerability'] = 1
        test_player.check_extra_powerups()
        test_player.check_extra_powerups()

        self.assertEqual(test_player.invulnerability_timer, 718)

    def test_check_extra_powerups_3(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.stats['speed'] = 1
        test_player.check_extra_powerups()

        self.assertEqual(test_player.speed_timer, 719)

    def test_check_extra_powerups_4(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((0, 0), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.stats['ghost'] = 1
        test_player.check_extra_powerups()

        self.assertEqual(test_player.ghost_timer, 719)

    def test_player_snap_to_grid_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((24, 10), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.player_snap_to_grid()

        self.assertEqual(test_player.rect.x, 0)
        self.assertEqual(test_player.rect.y, 0)

    def test_player_snap_to_grid_2(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((60, 74), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.player_snap_to_grid()

        self.assertEqual(test_player.rect.x, 50)
        self.assertEqual(test_player.rect.y, 50)

    def test_respawn_1(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((60, 74), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.respawn((0,0))

        self.assertEqual(test_player.rect.x, 0)
        self.assertEqual(test_player.rect.y, 0)

    def test_respawn_2(self):
        test_fields: Fields = Fields()
        test_player: Player = Player((60, 74), test_fields, Settings.P1_CONTROLS)
        test_player.load_assets(0)
        test_player.respawn((100,100))

        self.assertEqual(test_player.rect.x, 100)
        self.assertEqual(test_player.rect.y, 100)
if __name__ == '__main__':
    unittest.main()