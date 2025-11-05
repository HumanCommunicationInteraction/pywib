import unittest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import process_csv, import_pyModule

import_pyModule()

from pywib import number_of_clicks, click_slip

class TestData:
    dataFile = 'pywib/test/test_data/test_mouse.csv'
    expected_clicks = {
        'SESSION_A': 2,
        'SESSION_B': 2
    }
    expected_click_slips = {
        'SESSION_A': {'click_slips': 0,'longest_click_slip':0, 'shortest_click_slip': 0, 'average_click_slip': 0, 'average_click_slip_distance': 0},
        'SESSION_B': {'click_slips': 1, 'longest_click_slip': np.float64(25.0), 'shortest_click_slip': np.float64(25.0), 'average_click_slip': 1.0, 'average_click_slip_distance': np.float64(25.0)}
    }

class TestMouse(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create sample test data instead of relying on external CSV
        self.test_data = process_csv(TestData.dataFile)
        
    def test_number_of_clicks(self):
        clicks = number_of_clicks(self.test_data)
        self.assertEqual(clicks, TestData.expected_clicks)

    def test_click_slip(self):
        click_slips = click_slip(self.test_data)
        self.assertEqual(click_slips['SESSION_A'], TestData.expected_click_slips['SESSION_A'])
        self.assertEqual(click_slips['SESSION_B'], TestData.expected_click_slips['SESSION_B'])


if __name__ == '__main__':
    unittest.main()