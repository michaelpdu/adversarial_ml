import os, sys, time
from logging import *
from dna_manager import *
from pe_generator import *

class PEGeneratorRandom(PEGenerator):
    """"""

    def __init__(self, config):
        self.config_ = config
    
    def load_dna(self):
        self.dna_mgr_ = DNAManager()
        self.dna_mgr_.load_dna_files(os.path.join('DNA','DNA_PE','section_add'), DNAManager.DNA_TYPE_SECTION)
        self.dna_mgr_.load_dna_files(os.path.join('DNA','DNA_PE','imports_append'), DNAManager.DNA_TYPE_IMPORTF)

    def add_dna_random(self):
        self.modifier_.revert()
        dna_list_section = self.dna_mgr_.get_dna_random(self.config_['dna_manager']['random_section_count'], DNAManager.DNA_TYPE_SECTION)
        dna_list_imports = self.dna_mgr_.get_dna_random(self.config_['dna_manager']['random_imports_count'], DNAManager.DNA_TYPE_IMPORTF)
        
        # add section
        section_add_list = []
        for dna in dna_list_section:
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

        # append import functions
        imports_list = []
        for dna in dna_list_imports:
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

        # save generated PE
        tmp_file = '{}_{}'.format(self.filename_wo_ext, self.modifier_.get_hash_sha1())
        new_pe_path = os.path.join(self.dest_dir_, tmp_file)
        if not os.path.exists(new_pe_path):
            self.modifier_.save_pe(new_pe_path)
        return new_pe_path

    def generate(self, count):
        begin = time.time()
        for i in range(count):
            self.add_dna_random()
        delta = time.time() - begin
        msg = 'Generate {} sample randomly, time delta: {}'.format(count, delta)
        info(msg)
        print(msg)
