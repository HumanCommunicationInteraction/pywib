import unittest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import process_csv, import_pyModule

import_pyModule()

from pywib import movement_time, execution_time

DEBUG = False

class TestData:
    window_resize_error_file = 'test/test_data/test_window_resize_error.csv'
    window_resize_error_execution_time = 18100  # in milliseconds

class TestTiming(unittest.TestCase):

    def setUp(self):
        """Set up test data"""
        # Create sample test data instead of relying on external CSV
        
        if(DEBUG):
            self.test_data = process_csv(TestData.window_resize_error_file)
        else:
            self.test_data = process_csv('pywib/' + TestData.window_resize_error_file)
        
    def test_execution_time(self):
        """Test execution_time function"""
        exec_time = execution_time(self.test_data)
        self.assertIsInstance(exec_time, dict)
        for session_id, time in exec_time.items():
            self.assertIsInstance(session_id, str)
            self.assertGreaterEqual(time, 0)
            np.testing.assert_allclose(time, TestData.window_resize_error_execution_time, rtol=1e-5, atol=1e-8)

    def test_movement_time(self):
        """Test movement_time function"""
        move_time = movement_time(self.test_data)
        self.assertIsInstance(move_time, dict)
        for session_id, time in move_time.items():
            self.assertIsInstance(session_id, str)
            self.assertIsInstance(time, float)
            self.assertLessEqual(time, TestData.window_resize_error_execution_time)


if __name__ == '__main__':
    unittest.main()