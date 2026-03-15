import unittest
import numpy as np
import sys
import os
import pytest
sys.path.insert(0, os.path.dirname(__file__))
from utils import process_csv, import_pyModule

import_pyModule()

from pywib import typing_speed_metrics, typing_speed, backspace_usage, typing_durations,  ColumnNames

DEBUG = True

class TestData:
    if(DEBUG):
        dataFile = 'test/test_data/test_mouse_keyboard.csv'
    else:
        dataFile = 'pywib/test/test_data/test_mouse_keyboard.csv'

    results = {
        "SESSION_A":{
            "speed": [float((1/((1750792681050 - 1750792680900)/1000.0)) * 60.0), float(1/((1750792685500 - 1750792685400)/1000.0) * 60.0)],
            ColumnNames.BACKSPACE_USAGE: 0,
            "typing_durations": [float(1750792681050 - 1750792680900), float((1750792685500 - 1750792685400))],
            ColumnNames.TOTAL_CHARS: 2
        },
        "SESSION_B":{

            "speed": [float( (1/((1750792680980 - 1750792680920)/1000.0)) * 60.0), float( (4/((1750792686150 - 1750792685600)/1000.0)) * 60.0)],
            ColumnNames.BACKSPACE_USAGE: 3,
            "typing_durations": [float((1750792680980 - 1750792680920)), float((1750792686150 - 1750792685600))],
            ColumnNames.TOTAL_CHARS: 5
        },
        "ALL":{
            ColumnNames.BACKSPACE_USAGE:3,
            "typing_durations":[float(1750792681050 - 1750792680900), float((1750792685500 - 1750792685400)), float((1750792680980 - 1750792680920)), float((1750792686150 - 1750792685600))]
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
            expected_speeds = TestData.results[session_id]["speed"]
            for s, e in zip(speeds, expected_speeds):
                self.assertAlmostEqual(s, e, places=2)

    def test_typing_speed_df(self):
        """Test typing_speed function for DataFrame input"""
        df_session_b = self.test_data[self.test_data['sessionId'] == 'SESSION_B']
        speed = typing_speed(df_session_b, per_traces=False)
        self.assertEqual(speed, (6/(2500/1000)) * 60.0)

    def test_backspace_usage(self):
        """Test backspace_usage function"""
        backspace_stats = backspace_usage(self.test_data)
        for session_id, usage in backspace_stats.items():
            self.assertEqual(usage, TestData.results[session_id][ColumnNames.BACKSPACE_USAGE])

    def test_backspace_usage_df(self):
        """Test backspace_usage function using a singe DF withotut traces"""
        backspace_stats = backspace_usage(self.test_data, per_trace=False)
        self.assertEqual(backspace_stats, TestData.results["ALL"][ColumnNames.BACKSPACE_USAGE])

    def test_typing_speed_df(self):
        """Test typing_speed function for DataFrame input"""
        df_session_b = self.test_data[self.test_data['sessionId'] == 'SESSION_B']
        speed = typing_speed(df_session_b, per_traces=False)
        self.assertEqual(speed, (5/(((1750792686150 - 1750792685600) + (1750792680980 - 1750792680920))/1000.0)) * 60.0)

    def test_typing_speed_metrics(self):
        """Test typing_speed_metrics function"""
        metrics = typing_speed_metrics(self.test_data)
        for session_id, metric in metrics.items():
            expected_speeds = TestData.results[session_id]["speed"]
            avg_expected_speed = sum(expected_speeds) / len(expected_speeds)
            self.assertAlmostEqual(metric["average_typing_speed"], avg_expected_speed, places=2)
            self.assertEqual(metric[ColumnNames.TOTAL_CHARS], TestData.results[session_id][ColumnNames.TOTAL_CHARS])


    def test_typing_durations(self):
        """Test typing durations function"""
        t_durations = typing_durations(self.test_data, per_traces=True)
        for session_id, durations in t_durations.items():
            i = 0
            for duration in durations:          
                self.assertAlmostEqual(duration, TestData.results[session_id]["typing_durations"][i])
                i+=1

    def test_typing_durations_df(self):
        """Test typing durations function for a single DataFrame"""
        t_durations = typing_durations(self.test_data, per_traces=False)
        i = 0
        for durations in t_durations:
            self.assertAlmostEqual(durations, TestData.results["ALL"]["typing_durations"][i])
            i+=1        
                

if __name__ == '__main__':
    unittest.main()