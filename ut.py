import os, sys
import unittest
import tlsh
from logging import *

sys.path.append(os.path.join(os.path.dirname(__file__),'UT'))
# from ut_trendx_predictor import TrendXPredictorTestCase
from ut_dna_manager import DNAManagerTestCase
from ut_housecallx_report import HouseCallXReportTestCase
from ut_trendx_wrapper import TrendXWrapperTestCase
from ut_pe_generator import PEGeneratorTestCase
from ut_workflow import AdversaryWorkflowTestCase
from ut_tlsh import TLSHTestCase
from ut_adversary_tlsh import TLSHAdversaryTestCase

def suite():  
    suite = unittest.TestSuite()
    # TrendXPredictor Test Cases
    # suite.addTest(TrendXPredictorTestCase("test_script_adversary"))
    # suite.addTest(TrendXPredictorTestCase("test_pe_adversary"))

    # # DNAManager Test Cases
    # suite.addTest(DNAManagerTestCase("test_load_dna"))
    # suite.addTest(DNAManagerTestCase("test_load_dna_random"))
    # suite.addTest(DNAManagerTestCase("test_generate_random_indexes"))
    
    # # HouseCallXReport Test Cases
    # suite.addTest(HouseCallXReportTestCase("test_get_scores"))

    # # TrendX Wrapper Test Cases
    # if sys.version_info.major >= 3:
    #     suite.addTest(TrendXWrapperTestCase("test_scan_pe_file"))
    #     suite.addTest(TrendXWrapperTestCase("test_scan_pe_dir"))
    #     suite.addTest(TrendXWrapperTestCase("test_scan_pe_list"))
    # else:
    #     suite.addTest(TrendXWrapperTestCase("test_scan_script_file"))
    #     suite.addTest(TrendXWrapperTestCase("test_scan_script_dir"))
    #     suite.addTest(TrendXWrapperTestCase("test_scan_script_list"))

    # # PEGeneratorRandom Test Cases
    # if sys.version_info.major >= 3:
    #     suite.addTest(PEGeneratorTestCase("test_generate"))
    #     # suite.addTest(PEGeneratorRandomTestCase("test_generate_imports"))
    # else:
    #     pass

    # # AdversaryWorkflow Test Case
    # if sys.version_info.major >= 3:
    #     suite.addTest(AdversaryWorkflowTestCase("test_process"))
    #     suite.addTest(AdversaryWorkflowTestCase("test_start"))
    #     suite.addTest(AdversaryWorkflowTestCase("test_attack"))
    # else:
    #     pass

    # # TLSH Test Case
    # suite.addTest(TLSHTestCase("test_get_tlsh"))
    # suite.addTest(TLSHTestCase("test_gen_csv_for_file"))
    # suite.addTest(TLSHTestCase("test_gen_csv_for_dir"))
    # suite.addTest(TLSHTestCase("test_gen_and_scan_csv"))
    # suite.addTest(TLSHTestCase("test_tlsh_wrapper_scan"))

    # TLSHAdversary Test Case
    suite.addTest(TLSHAdversaryTestCase("test_process_pe_in_ga"))

    return suite
  
if __name__ == "__main__":
    basicConfig(filename='adversary_ml_ut_{}.log'.format(os.getpid()), format='[%(asctime)s][%(process)d.%(thread)d][%(levelname)s] - %(message)s', level=DEBUG)
    unittest.main(defaultTest = 'suite')
