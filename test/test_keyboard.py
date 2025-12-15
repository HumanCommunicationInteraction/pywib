import unittest
import numpy as np
import sys
import os
import pytest
sys.path.insert(0, os.path.dirname(__file__))
from utils import process_csv, import_pyModule

import_pyModule()

from pywib import typing_speed_metrics, typing_speed, backspace_usage

DEBUG = True

class TestData:
    if(DEBUG):
        dataFile = 'test/test_data/test_mouse_keyboard.csv'
    else:
        dataFile = 'pywib/test/test_data/test_mouse_keyboard.csv'

    reults = {
        "SESSION_A":{
            "speed": [float(400.0), float(600.0)],
            "backspace_usage": 0,
            "typing_durations": [120, 130, 115, 125, 135]
        },
        "SESSION_B":{
            "speed": [float(1000.0), float(450.0)],
            "backspace_usage": 3,
            "typing_durations": [100, 110, 90, 95, 105]
        }
    }

class TestKeyboard(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create sample test data instead of relying on external CSV
        self.test_data = process_csv(TestData.dataFile)
        
    def test_typing_speed(self):
        """Test typing_speed function"""
        speed = typing_speed(self.test_data, per_traces=True)
        for session_id, speeds in speed.items():
            expected_speeds = TestData.reults[session_id]["speed"]
            for s, e in zip(speeds, expected_speeds):
                self.assertAlmostEqual(s, e, places=2)

    def test_backspace_usage(self):
        """Test backspace_usage function"""
        backspace_stats = backspace_usage(self.test_data)
        for session_id, usage in backspace_stats.items():
            self.assertEqual(usage, TestData.reults[session_id]["backspace_usage"])

    def test_typing_speed_df(self):
        """Test typing_speed function for DataFrame input"""
        df_session_b = self.test_data[self.test_data['sessionId'] == 'SESSION_B']
        speed = typing_speed(df_session_b, per_traces=False)
        self.assertEqual(speed, 8/2500/1000 * 60.0)

if __name__ == '__main__':
    unittest.main()