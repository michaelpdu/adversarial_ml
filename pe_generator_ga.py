import os, sys
from dna_manager import *
from pe_generator import *

class PEGeneratorGA(PEGenerator):
    """"""

    def __init__(self, config):
        self.config_ = config
    
    def load_dna(self):
        self.dna_mgr_ = DNAManager()
        self.dna_mgr_.load_dna_files(os.path.join('DNA','DNA_PE','section_add'))
    
    def add_section_random(self):
        dna_list = self.dna_mgr_.get_dna_random(self.config_['dna_manager']['random_count'])
        section_add_list = []
        for dna in dna_list:
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

        tmp_file = '{}_{}'.format(self.filename_wo_ext, self.modifier_.get_hash_sha1())
        new_pe_path = os.path.join(self.dest_dir_, tmp_file)
        self.modifier_.save_pe(new_pe_path)
        return new_pe_path

    def generate(self, count):
        for i in range(count):
            print("Generate {} sample randomly".format(i+1))
            self.add_section_random()

