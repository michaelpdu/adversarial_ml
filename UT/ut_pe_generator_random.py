import os, sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pe_generator_random import PEGeneratorRandom


class PEGeneratorRandomTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_generate(self):
        generator = PEGeneratorRandom({"dna_manager": {"random_count": 50}})
        generator.load_sample(os.path.join('UT', 'staff', 'pe', 'malicious_pe.ex_'))
        generator.load_dna()
        generator.set_dest_dir(os.path.join('new_generated_samples', 'UT', 'pe'))
        generator.generate(5)

