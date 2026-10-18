"""Run retained regressions and evolution-02 checks against the candidate."""
import sys
import unittest
from pathlib import Path

checks = Path(__file__).resolve().parent
sys.path.insert(0, str(checks))
sys.path.insert(0, str(checks / 'legacy'))
suite = unittest.TestSuite()
for directory in (checks / 'legacy', checks):
    suite.addTests(unittest.TestLoader().discover(
        str(directory), pattern='test_*.py', top_level_dir=str(directory)))
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
