import os, sys, json, shutil
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from start import AdversaryWorkflow, start, attack

class AdversaryWorkflowTestCase(unittest.TestCase):
    def setUp(self):
        with open('config.json', 'r') as fh:
            self.config_ = json.load(fh)

    def tearDown(self):
        pass
    
    def test_process_trendx_pe_bruteforce(self):
        print('>> AdversaryWorkflowTestCase.test_process_trendx_pe_bruteforce')
        config = self.config_
        config['common']['enable_system_cpu'] = False
        config['common']['use_cpu_count'] = 2
        config['common']['samples'] = "UT/staff/pe/malicious/malicious_pe.ex_"
        config['common']['algorithm'] = 'bruteforce'
        config['common']['target'] = 'trendx_pe'
        config['pe_generator_random']['count'] = 5
        config['pe_generator_random']['round'] = 1
        config['cuckoo']['enable'] = False
        adv = AdversaryWorkflow(config)
        generate_count, bypassed_count = adv.process(0)
        assert(generate_count == 5)

        config['common']['samples'] = "UT/staff/pe/malicious"
        adv = AdversaryWorkflow(config)
        generate_count, bypassed_count = adv.process(0)
        sample_count = len(os.listdir(config['common']['samples']))
        assert(generate_count == 5*sample_count)

    def test_process_trendx_script_bruteforce(self):
        pass
    
    def test_process_trendx_pe_ga(self):
        pass

    def test_process_trendx_script_ga(self):
        pass

    def test_process_tlsh_pe_bruteforce(self):
        pass

    def test_process_tlsh_script_bruteforce(self):
        pass

    def test_process_tlsh_pe_ga(self):
        print('>> AdversaryWorkflowTestCase.test_process_tlsh_pe_ga')
        config = self.config_
        config['common']['enable_system_cpu'] = False
        config['common']['use_cpu_count'] = 2
        config['common']['samples'] = "UT/staff/pe/malicious/malicious_pe.ex_"
        config['common']['algorithm'] = 'ga'
        config['common']['target'] = 'tlsh_pe'
        config['genetic_algorithm']['dna_size'] = 10
        config['genetic_algorithm']['generations'] = 20
        config['cuckoo']['enable'] = False
        adv = AdversaryWorkflow(config)
        generate_count, bypassed_count = adv.process(0)
        assert(generate_count == 5)

        # config['common']['samples'] = "UT/staff/pe/malicious"
        # adv = AdversaryWorkflow(config)
        # generate_count, bypassed_count = adv.process(0)
        # sample_count = len(os.listdir(config['common']['samples']))
        # assert(generate_count == 5*sample_count)

    def test_process_tlsh_script_ga(self):
        pass

    def test_start(self):
        print('>> AdversaryWorkflowTestCase.test_start')
        config = self.config_
        config['common']['enable_system_cpu'] = False
        config['common']['use_cpu_count'] = 2
        config['common']['samples'] = "UT/staff/pe/malicious/malicious_pe.ex_"
        config['common']['algorithm'] = 'ga'
        config['common']['target'] = 'tlsh_pe'
        config['genetic_algorithm']['dna_size'] = 10
        config['genetic_algorithm']['population_size'] = 11
        config['genetic_algorithm']['generations'] = 12
        config['cuckoo']['enable'] = False
        gen_count, bypassed_count = start(0, config)
        # print('generated count: {}, bypassed count: {}'.format(gen_count, bypassed_count))
        assert(gen_count == 132)

        config['common']['algorithm'] = 'bruteforce'
        config['pe_generator_random']['count'] = 5
        config['pe_generator_random']['round'] = 2
        gen_count, bypassed_count = start(0, config)
        assert(gen_count == 10)

    def test_attack(self):
        print('>> AdversaryWorkflowTestCase.test_attack')
        config = self.config_
        config['common']['enable_system_cpu'] = False
        config['common']['use_cpu_count'] = 2
        config['common']['samples'] = "UT/staff/pe/malicious"
        config['pe_generator_random']['count'] = 5
        config['pe_generator_random']['round'] = 2
        config['cuckoo']['enable'] = False
        sample_count = len(os.listdir(config['common']['samples']))
        total_gen, total_bypassed = attack(config)
        assert(total_gen == 20*sample_count)
