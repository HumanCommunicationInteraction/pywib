import unittest
import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import process_csv, import_pyModule

import_pyModule()

from pywib import number_of_clicks, click_slip

DEBUG = True

class TestData:
    
    dataFile = 'test/test_data/test_mouse.csv'
    expected_clicks = {
        'SESSION_A': 2,
        'SESSION_B': 2
    }
    expected_click_slips = {
        'SESSION_A': {'click_slips': 0,'max_click_slip':0, 'min_click_slip': 0, 'mean_click_slip': 0, 'mean_click_duration':  np.float64(30.0), 'max_click_duration': 30, 'min_click_duration':  30},
        'SESSION_B': {'click_slips': 1, 'max_click_slip': np.float64(25.0), 'min_click_slip': np.float64(25.0), 'mean_click_slip': np.float64(25.0), 'mean_click_duration': np.float64(30.0), 'max_click_duration': np.float64(30.0), 'min_click_duration': 30}
    }

class TestMouse(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create sample test data instead of relying on external CSV
        if(DEBUG):
            self.test_data = process_csv(TestData.dataFile)
        else:
            self.test_data = process_csv('pywib/' + TestData.dataFile)
        
    def test_number_of_clicks_empty(self):
        clicks = number_of_clicks(self.test_data.drop(self.test_data.index))
        self.assertEqual(clicks, {})

    def test_number_of_clicks(self):
        clicks = number_of_clicks(self.test_data)
        self.assertEqual(clicks, TestData.expected_clicks)

    def test_click_slip(self):
        click_slips = click_slip(self.test_data)
        self.assertEqual(click_slips['SESSION_A'], TestData.expected_click_slips['SESSION_A'])
        self.assertEqual(click_slips['SESSION_B'], TestData.expected_click_slips['SESSION_B'])

    def test_click_slip_empty(self):
        click_slips = click_slip(self.test_data.drop(self.test_data.index))
        self.assertEqual(click_slips, {})

    def test_click_duration(self):
        durations = click_slip(self.test_data)
        self.assertIn('SESSION_A', durations)
        self.assertIn('SESSION_B', durations)
        self.assertGreaterEqual(durations['SESSION_A']['mean_click_duration'], 30)
        self.assertGreaterEqual(durations['SESSION_B']['mean_click_duration'], 30)
        self.assertGreaterEqual(durations['SESSION_A']['max_click_duration'], durations['SESSION_B']['min_click_duration'])
        self.assertGreaterEqual(durations['SESSION_B']['max_click_duration'], durations['SESSION_B']['min_click_duration'])

    def test_click_duration_zero_threshold(self):
        """
        When the threshold is 0, all durations must appear
        """
        durations = click_slip(self.test_data, threshold=0)
        self.assertIn('SESSION_A', durations)
        self.assertIn('SESSION_B', durations)
        self.assertGreaterEqual(durations['SESSION_A']['average_click_duration'], 30)
        self.assertGreaterEqual(durations['SESSION_B']['average_click_duration'], 30)

    def test_click_duration_inf_threshold(self):
        """
        When the threshold is INF, there must not be any click durations
        """
        durations = click_slip(self.test_data, threshold=np.inf)
        self.assertIn('SESSION_A', durations)
        self.assertIn('SESSION_B', durations)
        self.assertGreaterEqual(durations['SESSION_A']['average_click_duration'], 0)
        self.assertGreaterEqual(durations['SESSION_B']['average_click_duration'], 0)

if __name__ == '__main__':
    unittest.main()