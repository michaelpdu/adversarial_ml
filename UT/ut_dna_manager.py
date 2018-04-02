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
        dna_mgr.load_dna_files_partial(os.path.join('DNA','DNA_PE','section_add'), 5, 30, DNAManager.DNA_TYPE_SECTION)
        dna_list = dna_mgr.get_dna(DNAManager.DNA_TYPE_SECTION)
        assert(len(dna_list) == 30)

        dna_mgr_2 = DNAManager()
        dna_mgr_2.load_dna_files_partial(os.path.join('DNA','DNA_PE','section_add'), 5, 30, DNAManager.DNA_TYPE_SECTION)
        dna_list_2 = dna_mgr.get_dna(DNAManager.DNA_TYPE_SECTION)
        assert(self.compare_two_list(dna_list, dna_list_2))
    
    def test_load_dna_random(self):
        dna_mgr = DNAManager()
        dna_mgr.load_dna_files(os.path.join('DNA','DNA_PE','section_add'), DNAManager.DNA_TYPE_SECTION)
        dna_mgr.load_dna_files(os.path.join('DNA','DNA_PE','imports_append'), DNAManager.DNA_TYPE_IMPORTF)
        assert(len(dna_mgr.get_dna_random(40, DNAManager.DNA_TYPE_SECTION)) == 40)
        assert(len(dna_mgr.get_dna_random(50, DNAManager.DNA_TYPE_IMPORTF)) == 50)

    def test_generate_random_indexes(self):
        print('> test_generate_random_indexes')
        dna_mgr = DNAManager()
        print(dna_mgr.generate_random_indexes(10, 100))
        print(dna_mgr.generate_random_indexes(10, 100))
        print(dna_mgr.generate_random_indexes(10, 100))
        print(dna_mgr.generate_random_indexes(10, 100))
        print(dna_mgr.generate_random_indexes(10, 100))
