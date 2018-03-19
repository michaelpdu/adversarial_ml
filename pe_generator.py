import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from pe_modifier.pe_modifier import *

class PEGenerator(object):
    """"""

    def load_sample(self, sample_path):
        self.modifier_ = PEModifier()
        self.modifier_.load_pe(sample_path)
        dir_path, filename = os.path.split(sample_path)
        self.filename_wo_ext, ext = os.path.splitext(filename)

    def set_dest_dir(self, dest_dir):
        self.dest_dir_ = dest_dir
        if not os.path.exists(self.dest_dir_):
            os.makedirs(self.dest_dir_)

