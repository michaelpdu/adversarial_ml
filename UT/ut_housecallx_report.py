import os, sys
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools'))
from hcx_report import HouseCallXReport

class HouseCallXReportTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_get_scores(self):
        report_path = os.path.join('UT','staff','60_Report.log')
        scores = HouseCallXReport.get_scores(report_path)
        malicious_count = 0
        suspicious_count = 0
        normal_count = 0
        for key, value in scores.items():
            if value[0] == 2:
                malicious_count += 1
            elif value[0] == 1:
                suspicious_count += 1
            else:
                normal_count += 1
        # print('{},{},{}'.format(normal_count, suspicious_count, malicious_count))
        assert(normal_count == 0)
        assert(suspicious_count == 11)
        assert(malicious_count == 89)
