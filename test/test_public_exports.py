import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from utils import import_pyModule

import_pyModule()

import pywib
import pywib.core as core
import pywib.utils as utils


class TestPublicExports(unittest.TestCase):
    def test_root_all_has_unique_entries(self):
        self.assertEqual(len(pywib.__all__), len(set(pywib.__all__)))

    def test_root_all_symbols_are_resolvable(self):
        for name in pywib.__all__:
            self.assertTrue(
                hasattr(pywib, name),
                f"pywib.__all__ includes '{name}' but it is not importable from pywib",
            )

    def test_core_all_symbols_are_resolvable(self):
        for name in core.__all__:
            self.assertTrue(
                hasattr(core, name),
                f"pywib.core.__all__ includes '{name}' but it is not importable from pywib.core",
            )

    def test_utils_all_symbols_are_resolvable(self):
        for name in utils.__all__:
            self.assertTrue(
                hasattr(utils, name),
                f"pywib.utils.__all__ includes '{name}' but it is not importable from pywib.utils",
            )

    def test_core_exports_are_available_from_root(self):
        missing = [name for name in core.__all__ if name not in pywib.__all__]
        self.assertEqual(
            missing,
            [],
            f"pywib.core exports missing from pywib root __all__: {missing}",
        )


if __name__ == "__main__":
    unittest.main()
