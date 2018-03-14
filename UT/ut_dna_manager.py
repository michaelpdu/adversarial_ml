import os, sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dna_manager import DNAManager

class DNAManagerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def compare_two_list(self, list1, list2):
        if len(list1) == len(list2):
            for i in range(len(list1)):
                if list1[i] != list2[i]:
                    return False
            return True
        else:
            return False

    def test_load_dna(self):
        dna_mgr = DNAManager()
        dna_mgr.load_dna_files(os.path.join('DNA','DNA_PE','section_add'), 5, 30)
        dna_list = dna_mgr.get_dna()
        assert(len(dna_list) == 30)

        dna_mgr_2 = DNAManager()
        dna_mgr_2.load_dna_files(os.path.join('DNA','DNA_PE','section_add'), 5, 30)
        dna_list_2 = dna_mgr.get_dna()
        assert(self.compare_two_list(dna_list, dna_list_2))
    
    def test_load_dna_random(self):
        dna_mgr = DNAManager()
        dna_mgr.load_all_dna_files(os.path.join('DNA','DNA_PE','section_add'))
        assert(len(dna_mgr.get_dna_random(40)) == 40)
