import unittest
import numpy as np
import sys
import os
import pytest
sys.path.insert(0, os.path.dirname(__file__))
from utils import process_csv, import_pyModule

import_pyModule()

from pywib import typing_speed_metrics, typing_speed, backspace_usage

DEBUG = False

class TestData:
    if(DEBUG):
        dataFile = 'test/test_data/test_mouse_keyboard.csv'
    else:
        dataFile = 'pywib/test/test_data/test_mouse_keyboard.csv'

    reults = {
        "SESSION_A":{
            "speed": [100.0, 110.0, 105.0],
            "backspace_usage": 0,
            "typing_durations": [120, 130, 115, 125, 135]
        },
        "SESSION_B":{
            "speed": [120.0, 130.0, 125.0],
            "backspace_usage": 2,
            "typing_durations": [100, 110, 90, 95, 105]
        }
    }

class TestKeyboard(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create sample test data instead of relying on external CSV
        self.test_data = process_csv(TestData.dataFile)
        
    def test_typing_speed_metrics(self):
        """Test typing_speed_metrics function"""
        speed = typing_speed(self.test_data)
        self.assertIsInstance(speed, dict)

    def test_backspace_usage(self):
        """Test backspace_usage function"""
        backspace_stats = backspace_usage(self.test_data)
        for session_id, usage in backspace_stats.items():
            self.assertEqual(usage, TestData.reults[session_id]["backspace_usage"])

if __name__ == '__main__':
    unittest.main()