import os, sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__),'UT'))
# from ut_trendx_predictor import TrendXPredictorTestCase
from ut_dna_manager import DNAManagerTestCase
from ut_housecallx_report import HouseCallXReportTestCase
from ut_trendx_wrapper import TrendXWrapperTestCase
from ut_pe_generator_random import PEGeneratorRandomTestCase

def suite():  
    suite = unittest.TestSuite()
    # TrendXPredictor Test Cases
    # suite.addTest(TrendXPredictorTestCase("test_script_adversary"))
    # suite.addTest(TrendXPredictorTestCase("test_pe_adversary"))

    # DNAManager Test Cases
    suite.addTest(DNAManagerTestCase("test_load_dna"))
    suite.addTest(DNAManagerTestCase("test_load_dna_random"))
    
    # HouseCallXReport Test Cases
    suite.addTest(HouseCallXReportTestCase("test_get_scores"))

    # TrendX Wrapper Test Cases
    if sys.version_info.major >= 3:
        suite.addTest(TrendXWrapperTestCase("test_scan_pe_file"))
        suite.addTest(TrendXWrapperTestCase("test_scan_pe_dir"))
        suite.addTest(TrendXWrapperTestCase("test_scan_pe_list"))
    else:
        suite.addTest(TrendXWrapperTestCase("test_scan_script_file"))
        suite.addTest(TrendXWrapperTestCase("test_scan_script_dir"))
        suite.addTest(TrendXWrapperTestCase("test_scan_script_list"))

    # PEGeneratorRandom Test Cases
    if sys.version_info.major >= 3:
        suite.addTest(PEGeneratorRandomTestCase("test_generate"))

    return suite
  
if __name__ == "__main__":  
    unittest.main(defaultTest = 'suite')
