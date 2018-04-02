import os, sys, json
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pe_generator_random import PEGeneratorRandom


class PEGeneratorRandomTestCase(unittest.TestCase):
    def setUp(self):
        with open('config.json', 'r') as fh:
            self.config_ = json.load(fh)

    def tearDown(self):
        pass
    
    def test_generate(self):
        config = self.config_
        config['dna_manager']['random_section_count'] = 10
        generator = PEGeneratorRandom(config)
        generator.load_sample(os.path.join('UT', 'staff', 'pe', 'malicious', 'malicious_pe.ex_'))
        generator.load_dna()
        generator.set_dest_dir(os.path.join('new_generated_samples', 'UT', 'pe'))
        generator.generate(5)

    def test_generate_imports(self):
        config = self.config_
        config['dna_manager']['random_section_count'] = 0
        config['dna_manager']['random_imports_count'] = 10
        generator = PEGeneratorRandom(config)
        generator.load_sample(os.path.join('samples', 'Adversarial_baseline_samples', 'Baseline-22'))
        generator.load_dna()
        generator.set_dest_dir(os.path.join('new_generated_samples', 'UT', 'pe'))
        generator.generate(5)