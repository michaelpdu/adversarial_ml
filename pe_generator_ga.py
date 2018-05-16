import os, sys, time
from logging import *
from dna_manager import *
from pe_generator import *

class PEGeneratorGA(PEGenerator):
    """"""

    def __init__(self, config):
        self.config_ = config

    def load_dna(self):
        self.dna_mgr_ = DNAManager()
        self.dna_mgr_.load_dna_files(os.path.join('DNA','DNA_PE','section_add'), DNAManager.DNA_TYPE_SECTION)
        self.dna_mgr_.load_dna_files(os.path.join('DNA','DNA_PE','imports_append'), DNAManager.DNA_TYPE_IMPORTF)

    def generate(self, count):
        pass








