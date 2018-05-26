import os, sys, time
from logging import *
from dna_manager import *

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from pe_modifier.pe_modifier import *

class PEGenerator:
    """"""

    def __init__(self, config):
        self.config_ = config
    
    def load_sample(self, sample_path):
        self.modifier_ = PEModifier()
        self.modifier_.load_pe(sample_path)
        dir_path, filename = os.path.split(sample_path)
        self.filename_wo_ext, ext = os.path.splitext(filename)

    def set_dest_dir(self, dest_dir):
        self.dest_dir_ = dest_dir
        if not os.path.exists(self.dest_dir_):
            os.makedirs(self.dest_dir_)

    def load_dna(self):
        self.dna_mgr_ = DNAManager()
        self.dna_mgr_.load_dna_files(os.path.join('DNA','DNA_PE','section_add'), DNAManager.DNA_TYPE_SECTION)
        self.dna_mgr_.load_dna_files(os.path.join('DNA','DNA_PE','imports_append'), DNAManager.DNA_TYPE_IMPORTF)

    def generate_random(self, count):
        begin = time.time()
        for i in range(count):
            self.add_dna_random()
        delta = time.time() - begin
        msg = 'Generate {} sample randomly, time delta: {}'.format(count, delta)
        info(msg)
        print(msg)

    def generate_indexes(self, index_list):
        begin = time.time()
        new_file = self.add_dna_indexes(index_list)
        delta = time.time() - begin
        msg = 'Generate sample by indexes, time delta: {}'.format(delta)
        info(msg)
        # print(msg)
        return new_file

    def modify_section(self, section_list):
        # add section
        section_add_list = []
        for dna in section_list:
            lines = dna.strip().split('\n')
            cmd = lines[0]
            if cmd == 'section_add':
                str_list = lines[1].split(' ')
                int_list = []
                for s in str_list:
                    int_list.append(int(s))
                section_add_list.append(int_list)
            else:
                pass
        if len(section_add_list) > 0:
            self.modifier_.modify({'section_add_list': section_add_list})

    def modify_import_table(self, import_functions):
        # append import functions
        imports_list = []
        for dna in import_functions:
            lines = dna.strip().split('\n')
            cmd = lines[0]
            if cmd == 'imports_append':
                dllname = lines[1].strip()
                funcname = lines[2].strip()
                imports_list.append((dllname, funcname))
            else:
                pass
        if len(imports_list) > 0:
            self.modifier_.modify({'imports_append_list': imports_list})

    def add_dna_random(self):
        # revert modifier
        self.modifier_.revert()

        # 
        dna_list_section = self.dna_mgr_.get_dna_random(self.config_['dna_manager']['random_section_count'], DNAManager.DNA_TYPE_SECTION)
        self.modify_section(dna_list_section)
        dna_list_imports = self.dna_mgr_.get_dna_random(self.config_['dna_manager']['random_imports_count'], DNAManager.DNA_TYPE_IMPORTF)
        self.modify_import_table(dna_list_imports)

        # save generated PE
        tmp_file = '{}_{}'.format(self.filename_wo_ext, self.modifier_.get_hash_sha1())
        new_pe_path = os.path.join(self.dest_dir_, tmp_file)
        if not os.path.exists(new_pe_path):
            self.modifier_.save_pe(new_pe_path)
        return new_pe_path

    def add_dna_indexes(self, index_list):
        # revert modifier
        self.modifier_.revert()

        # 
        dna_list_section = self.dna_mgr_.get_dna_indexes(index_list, DNAManager.DNA_TYPE_SECTION)
        self.modify_section(dna_list_section)
        dna_list_imports = self.dna_mgr_.get_dna_indexes(index_list, DNAManager.DNA_TYPE_IMPORTF)
        self.modify_import_table(dna_list_imports)

        # save generated PE
        tmp_file = '{}_{}'.format(self.filename_wo_ext, self.modifier_.get_hash_sha1())
        new_pe_path = os.path.join(self.dest_dir_, tmp_file)
        if not os.path.exists(new_pe_path):
            self.modifier_.save_pe(new_pe_path)
        return new_pe_path