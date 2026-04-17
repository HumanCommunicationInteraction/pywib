import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import process_csv, import_pyModule

import_pyModule()
from pywib import (velocity, velocity_metrics, acceleration, acceleration_metrics, jerkiness, jerkiness_metrics,
    path, auc, deviations,
    number_of_clicks, click_slip)

class TestAllMetrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = process_csv('test/test_data/test.csv')

    def test_velocity_metrics(self):
        vel_traces = velocity(self.df, per_traces=True)
        vel_metrics = velocity_metrics(self.df, vel_traces)
        self.assertIsInstance(vel_metrics, dict)
        for session in vel_metrics.values():
            self.assertIn('mean', session)
            self.assertIn('max', session)
            self.assertIn('min', session)

    def test_acceleration_metrics(self):
        acc_traces = acceleration(self.df, per_traces=True)
        acc_metrics = acceleration_metrics(self.df, acc_traces)
        self.assertIsInstance(acc_metrics, dict)
        for session in acc_metrics.values():
            self.assertIn('mean', session)
            self.assertIn('max', session)
            self.assertIn('min', session)

    def test_jerkiness_metrics(self):
        jerk_traces = jerkiness(self.df, per_traces=True)
        jerk_metrics = jerkiness_metrics(self.df, jerk_traces)
        self.assertIsInstance(jerk_metrics, dict)
        for session in jerk_metrics.values():
            self.assertIn('mean', session)
            self.assertIn('max', session)
            self.assertIn('min', session)

    def test_path(self):
        path_length = path(self.df)
        self.assertIsNotNone(path_length)

    def test_auc(self):
        auc_traces = auc(self.df)
        self.assertIsNotNone(auc_traces)

    def test_deviations(self):
        deviations_traces = deviations(self.df)
        self.assertIsNotNone(deviations_traces)

    def test_number_of_clicks(self):
        clicks = number_of_clicks(self.df)
        self.assertIsInstance(clicks, dict)

    def test_click_slip(self):
        click_slip_metrics = click_slip(self.df)
        self.assertIsInstance(click_slip_metrics, dict)

if __name__ == '__main__':
    unittest.main()