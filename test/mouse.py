import unittest
import numpy as np
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
        'SESSION_A': {'click_slips': 0,'longest_click_slip':0, 'shortest_click_slip': 0, 'average_click_slip': 0, 'average_click_slip_distance': 0, 'average_click_duration':  np.float64(30.0), 'max_click_duration':  np.float64(30.0), 'min_click_duration':  np.float64(30.0)},
        'SESSION_B': {'click_slips': 1, 'longest_click_slip': np.float64(25.0), 'shortest_click_slip': np.float64(25.0), 'average_click_slip': 1.0, 'average_click_slip_distance': np.float64(25.0), 'average_click_duration': np.float64(30.0), 'max_click_duration': np.float64(30.0), 'min_click_duration': np.float64(30.0)}
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

    def test_click_duration(self):
        durations = click_slip(self.test_data)
        self.assertIn('SESSION_A', durations)
        self.assertIn('SESSION_B', durations)
        self.assertGreaterEqual(durations['SESSION_A']['average_click_duration'], 30)
        self.assertGreaterEqual(durations['SESSION_B']['average_click_duration'], 30)
        self.assertGreaterEqual(durations['SESSION_A']['max_click_duration'], durations['SESSION_B']['min_click_duration'])
        self.assertGreaterEqual(durations['SESSION_B']['max_click_duration'], durations['SESSION_B']['min_click_duration'])


if __name__ == '__main__':
    unittest.main()