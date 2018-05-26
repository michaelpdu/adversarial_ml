import os, sys, json, shutil
import unittest
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools'))
from genetic_algorithm_basic import GeneticAlgorithmHelper

class TLSHAdversaryTestCase(unittest.TestCase):
    def setUp(self):
        with open('config.json', 'r') as fh:
            self.config_ = json.load(fh)

    def tearDown(self):
        pass
    
    def test_process_trendx_pe_bruteforce(self):
        pass
    
    def test_process_trendx_pe_ga(self):
        pass

    def test_process_trendx_script_bruteforce(self):
        pass

    def test_process_trendx_script_ga(self):
        pass