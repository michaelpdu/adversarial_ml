import os, sys
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools'))
from trendx_wrapper import TrendXWrapper

class TrendXWrapperTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_scan_pe_file(self):
        trendx = TrendXWrapper({})
        hcx_path = os.path.join('tools', 'housecallx', 'hcx1')
        trendx.set_hcx(hcx_path)
        try:
            decision, prob = trendx.scan_pe_file(os.path.join('UT', 'staff', 'pe', 'malicious_pe.ex_'))
        except Exception as e:
            assert(str(e) == "TrendXWrapper.scan_pe_file does not implemented!")

    def test_scan_pe_dir(self):
        trendx = TrendXWrapper({})
        hcx_path = os.path.join('tools', 'housecallx', 'hcx1')
        trendx.set_hcx(hcx_path)
        sample_dir = os.path.abspath(os.path.join('UT', 'staff', 'pe'))
        # print(sample_dir)
        scores = trendx.scan_pe_dir(sample_dir)
        print(scores)
        for key, value in scores.items():
            if 'normal_pe' in key:
                assert(value[0] < 2)
            elif 'malicious_pe' in key:
                assert(value[0] == 2)
            else:
                pass
    
    def test_scan_pe_list(self):
        trendx = TrendXWrapper({})
        hcx_path = os.path.join('tools', 'housecallx', 'hcx1')
        trendx.set_hcx(hcx_path)
        try:
            sample_list = [os.path.join('UT', 'staff', 'pe', 'malicious_pe.ex_'), os.path.join('UT', 'staff', 'pe', 'normal_pe.ex_')]
            scores = trendx.scan_pe_list(sample_list)
        except Exception as e:
            assert(str(e) == "TrendXWrapper.scan_pe_list does not implemented!")
    
    def test_scan_script_file(self):
        trendx = TrendXWrapper({})
        decision, prob = trendx.scan_script_file(os.path.join('UT', 'staff', 'script', 'normal_script.js_'))
        print('decision: {}, prob: {}'.format(decision, prob))
        # assert(decision == 1)
    
    def test_scan_script_dir(self):
        trendx = TrendXWrapper({})
        scores = trendx.scan_script_dir(os.path.join('UT', 'staff', 'script'))
        print(scores)

    def test_scan_script_list(self):
        trendx = TrendXWrapper({})
        scores = trendx.scan_script_list([os.path.join('UT', 'staff', 'script', 'normal_script.js_'), os.path.join('UT', 'staff', 'script', 'normal_script_2.js_')])
        print(scores)