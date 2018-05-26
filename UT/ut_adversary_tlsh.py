import os, sys, json, shutil
import unittest
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools'))
from adversary_tlsh import TLSHAdversary
from genetic_algorithm_basic import GeneticAlgorithmHelper

class TLSHAdversaryTestCase(unittest.TestCase):
    def setUp(self):
        with open('config.json', 'r') as fh:
            self.config_ = json.load(fh)

    def tearDown(self):
        pass
    
    def test_process_pe_in_ga(self):
        self.config_['tlsh']['scan_type'] = TLSHAdversary.SCAN_TYPE_BINARY
        self.config_['genetic_algorithm']['dna_size'] = 10
        self.config_['genetic_algorithm']['generations'] = 15
        adv = TLSHAdversary(self.config_)
        adv.set_malicious_file('UT/staff/pe/malicious/malicious_pe.ex_')
        # prepare algrithm helper and set DNA size in each group
        helper = GeneticAlgorithmHelper(self.config_['genetic_algorithm'])
        helper.set_adv(adv)
        helper.set_calc_callback(adv.calc_tlsh)
        helper.set_msg_callback(adv.display_message)
        # evolution
        most_valuable_dna, max_value = helper.evolution()
        print('*** In this evolution, most valuable DNA: {}, maximium value: {}'.format(str(most_valuable_dna), max_value))