import os, sys, json, shutil
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tools'))
from tlsh_tool.tlsh_tool import *
from tlsh_wrapper import *

class TLSHTestCase(unittest.TestCase):
    def setUp(self):
        self.pre_dir = os.getcwd()
        with open('config.json', 'r') as fh:
            self.config_ = json.load(fh)

    def tearDown(self):
        pass
    
    def test_get_tlsh(self):
        tlsh_hash = get_tlsh("UT/staff/pe/malicious/malicious_pe.ex_")
        assert('6D845B2673FA6448E41679FBDE548889912A7DBA1E038F573139734D9877393CEC282C' == tlsh_hash)
    
    def test_gen_csv_for_file(self):
        output = 'UT/output/csv_for_file'
        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs(output)
        gen_csv_for_file("UT/staff/pe/malicious/malicious_pe.ex_", output)
        csv_file = os.path.join(output, 'file_tlsh_malicious_pe.ex__6D845B2673FA6448E41679FBDE548889912A7DBA1E038F573139734D9877393CEC282C.csv')
        assert(os.path.exists(csv_file))
        with open(csv_file, 'r') as fh:
            content = fh.read()
        assert(content == 'UT/staff/pe/malicious/malicious_pe.ex_,6D845B2673FA6448E41679FBDE548889912A7DBA1E038F573139734D9877393CEC282C\n')

    def test_gen_csv_for_dir(self):
        output = 'UT/output/csv_for_dir'
        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs(output)
        gen_csv_for_dir("UT/staff/pe/malicious/", output)
        csv_file = os.path.join(output, 'dir_tlsh_malicious.csv')
        assert(os.path.exists(csv_file))
        with open(csv_file, 'r') as fh:
            content = fh.read()
        assert(content == 'UT/staff/pe/malicious/malicious_pe_2.ex_,6D845B2673FA6448E41679FBDE548889912A7DBA1E038F573139734D9877393CEC282C\nUT/staff/pe/malicious/malicious_pe.ex_,6D845B2673FA6448E41679FBDE548889912A7DBA1E038F573139734D9877393CEC282C\n')

    def test_gen_and_scan_csv(self):
        # gen for file
        output = 'UT/output/csv_for_file'
        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs(output)
        csv_file = gen_csv("UT/staff/pe/malicious/malicious_pe.ex_", output)
        assert(csv_file == 'UT/output/csv_for_file/file_tlsh_malicious_pe.ex__6D845B2673FA6448E41679FBDE548889912A7DBA1E038F573139734D9877393CEC282C.csv')
        csv_file = os.path.abspath(csv_file)
        previous_wd = os.getcwd()
        os.chdir(os.path.join(previous_wd, 'tools', 'tlsh_tool'))
        content = scan_csv(csv_file)
        os.chdir(previous_wd)
        assert(content == 'NEAR-MISS\t\tpat_29\t273\n')
        # gen for dir
        output = 'UT/output/csv_for_dir'
        if os.path.exists(output):
            shutil.rmtree(output)
        os.makedirs(output)
        csv_file = gen_csv("UT/staff/pe/malicious/", output)
        assert(csv_file == 'UT/output/csv_for_dir/dir_tlsh_malicious.csv')
        csv_file = os.path.abspath(csv_file)
        previous_wd = os.getcwd()
        os.chdir(os.path.join(previous_wd, 'tools', 'tlsh_tool'))
        content = scan_csv(csv_file)
        os.chdir(previous_wd)
        assert(content == 'NEAR-MISS\t\tpat_29\t273\nNEAR-MISS\t\tpat_29\t273\n')

    def test_tlsh_wrapper_scan(self):
        tlsh_wrapper = TLSHWrapper()
        tlsh_wrapper.set_middle_dir('UT/csv_dir')
        result = tlsh_wrapper.scan_file('UT/staff/pe/malicious/malicious_pe.ex_')
        assert(result == 273)
        result = tlsh_wrapper.scan_dir('UT/staff/pe/malicious')
        assert(result['UT/staff/pe/malicious/malicious_pe.ex_'] == 273)
        assert(result['UT/staff/pe/malicious/malicious_pe_2.ex_'] == 273)