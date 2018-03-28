import os, sys, json, shutil
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from workflow import AdversaryWorkflow, start, attack


class AdversaryWorkflowTestCase(unittest.TestCase):
    def setUp(self):
        with open('config.json', 'r') as fh:
            self.config_ = json.load(fh)

    def tearDown(self):
        pass
    
    def test_process(self):
        print('>> AdversaryWorkflowTestCase.test_process')
        config = self.config_
        config['common']['enable_system_cpu'] = False
        config['common']['use_cpu_count'] = 2
        config['common']['samples'] = "UT/staff/pe/malicious/malicious_pe.ex_"
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

        shutil.rmtree(config['common']['generated_dir'])
        config['common']['remove_not_bypassed'] = False
        config['common']['samples'] = "UT/staff/pe/malicious/malicious_pe.ex_"
        config['cuckoo']['enable'] = True
        config['common']['use_cpu_count'] = 1
        config['pe_generator_random']['count'] = 5
        config['pe_generator_random']['round'] = 2
        generate_count, bypassed_count = adv.process(0)

    def test_start(self):
        print('>> AdversaryWorkflowTestCase.test_start')
        config = self.config_
        config['common']['enable_system_cpu'] = False
        config['common']['use_cpu_count'] = 2
        config['common']['samples'] = "UT/staff/pe/malicious/malicious_pe.ex_"
        config['pe_generator_random']['count'] = 5
        config['pe_generator_random']['round'] = 2
        config['cuckoo']['enable'] = False
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
