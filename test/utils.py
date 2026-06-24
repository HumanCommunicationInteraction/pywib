import numpy as np
import pandas as pd
from collections import defaultdict

def import_pyModule():
    """
    Necessary to import the pywib package when running tests directly from the test/ folder.
    """
    import sys
    import os

    # If running tests from the repo (package not installed), add src/ to sys.path
    REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    SRC_PATH = os.path.join(REPO_ROOT, 'src')
    if SRC_PATH not in sys.path:
        sys.path.insert(0, SRC_PATH)

def process_csv(file_path):
    """
    Reads a semicolon-separated CSV file and processes it into matrices grouped by sessionId and sceneId.
    Args:
        file_path (str): Path to the CSV file.
    """
    # Read the CSV file with semicolon separator
    df = pd.read_csv(file_path, encoding='utf-8', sep=',')
    
    df['timeStamp'] = df['timeStamp'].astype(str).str.replace(',', '', regex=False)
    df['timeStamp'] = pd.to_numeric(df['timeStamp'], errors='coerce')
    return df

def csv_to_df_no_checks(file_path):
    """
    Reads a semicolon-separated CSV file into a DataFrame without any validation checks.
    Args:
        file_path (str): Path to the CSV file.
    """
    return pd.read_csv(file_path, encoding='utf-8', sep=',')

def assert_between_zero_inf(self, data, column):
        self.assertIn(column, data)
        self.assertGreaterEqual(data[column], 0)
        self.assertLessEqual(data[column], np.inf)