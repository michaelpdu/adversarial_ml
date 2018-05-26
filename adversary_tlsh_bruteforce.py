import numpy as np
from logging import *
from dna_manager import *
from pe_generator import *

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from tlsh_wrapper import *

class TLSHBruteforceAdversary:
    """"""

    def __init__(self, config):
        self.config_ = config
        # scan type, 0 - script, 1 - binary
        self.scan_type_ = self.config_['tlsh']['scan_type']
        self.generator_ = PEGenerator(self.config_)
        self.generator_.load_dna()
        self.generate_count_ = 0
        self.bypassed_count_ = 0
   
    def process_random(self, cpu_index, file_path):
        round = self.config_['pe_generator_random']['round']
        for i in range(round):
            print('CPU index: {}, Current round is {}'.format(cpu_index, i + 1))
            print('>> Attack {}'.format(file_path))

            #
            dir_path, filename = os.path.split(file_path)
            dest_dir = os.path.abspath(os.path.join(self.config_['common']['generated_dir'], str(os.getpid()), filename, str(i)))
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            self.generator_.load_sample(file_path)
            self.generator_.set_dest_dir(dest_dir)

            cur_count = self.config_['pe_generator_random']['count']
            self.generator_.generate_random(cur_count)
            self.generate_count_ += cur_count

            # scan in TLSH wrapper
            tlsh_wrapper = TLSHWrapper()
            tlsh_wrapper.set_middle_dir(os.path.join(self.config_['common']['generated_dir'], 'csv_dir', str(os.getpid()), filename, str(i)))
            scores = tlsh_wrapper.scan_dir(file_path)
            for file_name, dist in scores.items():
                if dist > 100:
                    self.bypassed_count_ += 1

        return (self.generate_count_, self.bypassed_count_)
