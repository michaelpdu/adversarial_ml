import os, sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from calc_trendx_prediction import TrendxAdversary

class TrendXPredictorTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_script_adversary(self):
        adv = TrendxAdversary()
        adv.set_malicious_file(mal_sample_file)
        new_generated_dir = 'new_generated_files'
        adv.set_scan_type(TrendxAdversary.SCAN_TYPE_SCRIPT)
        adv.set_generated_dir(os.path.join(new_generated_dir, 'JS'))
        helper = GeneticAlgorithmHelper(adv, dna_size)
        helper.set_dna_size(dna_size)
        adv.load_dna_files(current_dna_dir, start_index, dna_size)
        most_valuable_dna, max_value = helper.evolution()

    def test_pe_adversary(self):
        adv = TrendxAdversary()
        adv.set_malicious_file(mal_sample_file)
        new_generated_dir = 'new_generated_files'
        adv.set_scan_type(TrendxAdversary.SCAN_TYPE_BINARY)
        adv.set_generated_dir(os.path.join(new_generated_dir, 'PE'))
        adv.set_hcx_target_dir(os.path.join(new_generated_dir, 'hcx_target_dir_{}'.format(os.getpid())))
        adv.set_housecallx_path(housecallx_dir)
        helper.set_dna_size(dna_size)
        adv.load_dna_files(current_dna_dir, start_index, dna_size)
        most_valuable_dna, max_value = helper.evolution()