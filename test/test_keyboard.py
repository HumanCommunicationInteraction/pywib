import unittest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import process_csv, import_pyModule

import_pyModule()

from pywib import typing_speed_metrics, typing_speed

DEBUG = True

class TestData:
    if(DEBUG):
        dataFile = 'pywib/test/test_data/test_mouse_keyboard.csv'
    else:
        dataFile = 'test/test_data/test_mouse_keyboard.csv'

class TestKeyboard(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create sample test data instead of relying on external CSV
        self.test_data = process_csv(TestData.dataFile)
        
    def test_typing_speed_metrics(self):
        """Test typing_speed_metrics function"""
        speed = typing_speed(self.test_data)
        metrics = typing_speed_metrics(self.test_data)
        self.assertIsInstance(speed, dict)


if __name__ == '__main__':
    unittest.main()