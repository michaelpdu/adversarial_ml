import os, sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from workflow import AdversaryWorkflow, start, attack


class AdversaryWorkflowTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_process(self):
        print('>> AdversaryWorkflowTestCase.test_process')
        config = {
                    "common": {
                        "depth": 3,
                        "free_disk": 1024,
                        "enable_system_cpu": False,
                        "use_cpu_count": 2,
                        "samples": "UT/staff/pe/malicious/malicious_pe.ex_",
                        "generated_dir": "new_generated_samples"
                    }, 
                    "dna_manager": {
                        "random_count": 10
                    },
                    "pe_generator_random": {
                        "count": 5,
                        "round": 1
                    },
                    "trendx": {
                        "scan_type": 2,
                        "housecallx": "tools/housecallx"
                    },
                    "cuckoo": {
                        "enable": False
                    }
                }
        adv = AdversaryWorkflow(config)
        generate_count, bypassed_count = adv.process(0)
        assert(generate_count == 5)

        config = {
                    "common": {
                        "depth": 3,
                        "free_disk": 1024,
                        "enable_system_cpu": False,
                        "use_cpu_count": 2,
                        "samples": "UT/staff/pe/malicious",
                        "generated_dir": "new_generated_samples"
                    }, 
                    "dna_manager": {
                        "random_count": 10
                    },
                    "pe_generator_random": {
                        "count": 5,
                        "round": 1
                    },
                    "trendx": {
                        "scan_type": 2,
                        "housecallx": "tools/housecallx"
                    },
                    "cuckoo": {
                        "enable": False
                    }
                }
        adv = AdversaryWorkflow(config)
        generate_count, bypassed_count = adv.process(0)
        sample_count = len(os.listdir(config['common']['samples']))
        assert(generate_count == 5*sample_count)

    def test_start(self):
        print('>> AdversaryWorkflowTestCase.test_start')
        config = {
                    "common": {
                        "depth": 3,
                        "free_disk": 1024,
                        "enable_system_cpu": False,
                        "use_cpu_count": 2,
                        "samples": "UT/staff/pe/malicious/malicious_pe.ex_",
                        "generated_dir": "new_generated_samples"
                    }, 
                    "dna_manager": {
                        "random_count": 10
                    },
                    "pe_generator_random": {
                        "count": 5,
                        "round": 2
                    },
                    "trendx": {
                        "scan_type": 2,
                        "housecallx": "tools/housecallx"
                    },
                    "cuckoo": {
                        "enable": False
                    }
                }
        gen_count, bypassed_count = start(0, config)
        # print('[UT] Gen count: {}, Bypassed count: {}'.format(gen_count, bypassed_count))
        assert(gen_count == 10)

    def test_attack(self):
        print('>> AdversaryWorkflowTestCase.test_attack')
        config = {
                    "common": {
                        "UT": True,
                        "depth": 3,
                        "free_disk": 1024,
                        "enable_system_cpu": False,
                        "use_cpu_count": 2,
                        "samples": "UT/staff/pe/malicious",
                        "generated_dir": "new_generated_samples"
                    }, 
                    "dna_manager": {
                        "random_count": 10
                    },
                    "pe_generator_random": {
                        "count": 5,
                        "round": 2
                    },
                    "trendx": {
                        "scan_type": 2,
                        "housecallx": "tools/housecallx"
                    },
                    "cuckoo": {
                        "enable": False
                    }
                }
        sample_count = len(os.listdir(config['common']['samples']))
        total_gen, total_bypassed = attack(config)
        assert(total_gen == 20*sample_count)
