import unittest
import sys
import os

import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from utils import assert_between_zero_inf, process_csv, import_pyModule

import_pyModule()
from pywib import (extract_traces_by_session, velocity, acceleration, jerkiness, compute_space_time_diff)

# Cambiar a True solo al probar en desarrollo
DEBUG = True

class TestData:

    if(DEBUG):
        trainFiles = 'test/balabit_dataset/train'
    else:
        dataFile = 'pywib/test/balabit_dataset/train'


class TestBalabit(unittest.TestCase):
    
    def setUp(self):
        #  First obtain all datasets
        self.traces = extract_traces_by_session(TestData.trainFiles)
    

if __name__ == '__main__':
    unittest.main()