import numpy as np
from logging import *
from dna_manager import *
from pe_generator import *

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from tlsh_wrapper import *

class TLSHGAAdversary:
    """"""

    SCAN_TYPE_SCRIPT = 0
    SCAN_TYPE_BINARY = 1

    def __init__(self, config):
        self.config_ = config
        # scan type, 0 - script, 1 - binary
        self.scan_type_ = self.config_['tlsh']['scan_type']
        self.generator_ = PEGenerator(self.config_)
        self.generator_.load_dna()
        self.generator_.set_dest_dir(self.config_['common']['generated_dir'])
        self.file2dna_ = {}
        self.file2dist_ = {}
        self.generate_count_ = 0
        self.bypassed_count_ = 0
        self.dna_start_index_ = int(self.config_['genetic_algorithm']['start_index'])

    def set_malicious_file(self, file_path):
        self.generator_.load_sample(file_path)

    # calc callback for genetic algorithm
    def calc_tlsh(self, dna_array):
        # clear
        self.file2dna_ = {}
        self.file2dist_ = {}

        dna_list = dna_array.tolist()
        # print(dna_list)
        prob_list = []
        tlsh_wrapper = TLSHWrapper()
        tlsh_wrapper.set_middle_dir(os.path.join(self.config_['common']['generated_dir'], 'csv_dir'))

        for dna in dna_list:
            # print item
            indexes = [index + self.dna_start_index_ for index, value in enumerate(dna) if value == 1]
            # print '>> '+str(indexes)
            # generate new PE
            new_file = self.generator_.generate_indexes(indexes)
            self.generate_count_ += 1
            self.file2dna_[new_file] = dna
            
            # use tlsh to scan new sample
            
            dist = tlsh_wrapper.scan_file(new_file)

            if dist > 100:
                self.bypassed_count_ += 1
            
            debug('Predict file: {}, and distance: {}'.format(new_file, dist))
            prob_list.append(dist)
        ret_array = np.array(prob_list)
        # return type is ndarray, and shape is (dna_size,)
        return ret_array

    # message callback
    def display_message(self, round, dna, value):
        file_path = ''
        for name, dna_value in self.file2dna_.items():
            if dna == dna_value:
                file_path = name
                break
        msg = "G{}: Most fitted DNA: {}, file: {} and value: {}".format(round, dna, file_path, value)
        info(msg)
        print(msg)
    
    def get_sample_info(self):
        return (self.generate_count_, self.bypassed_count_)