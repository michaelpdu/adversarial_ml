import os, sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from workflow import AdversaryWorkflow


class AdversaryWorkflowTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_process_file(self):
        print('>> AdversaryWorkflowTestCase.test_process_file')
        config = {
                    "common": {
                        "depth": 3,
                        "samples": "samples/Adversarial_baseline_samples",
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
                    }
                }

        adv = AdversaryWorkflow(config)
        adv.set_index(1)
        adv.process_file(os.path.join('UT','staff','pe','malicious','malicious_pe.ex_'))

    def test_process_dir(self):
        print('>> AdversaryWorkflowTestCase.test_process_dir')
        config = {
                    "common": {
                        "depth": 3,
                        "samples": "samples/Adversarial_baseline_samples",
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
                    }
                }

        adv = AdversaryWorkflow(config)
        adv.set_index(1)
        adv.process_dir(os.path.join('UT','staff','pe', 'malicious'))

    def test_attack(self):
        print('>> AdversaryWorkflowTestCase.test_attack')
        config = {
                    "common": {
                        "depth": 3,
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
                    }
                }

        adv = AdversaryWorkflow(config)
        adv.attack(2)

    def test_start(self):
        print('>> AdversaryWorkflowTestCase.test_start')
        config = {
                    "common": {
                        "depth": 3,
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
                    }
                }

        adv = AdversaryWorkflow(config)
        adv.start()