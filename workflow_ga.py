import os, sys
import time, json
from logging import *
from pe_generator_ga import *
from tools.trendx_wrapper import *


class AdversaryWorkflowGa:
    """"""

    def __init__(self, config):
        self.config_ = config

    def set_index(self, index):
        self.index_ = index

    def process_file(self, file_path):
        new_dna_dir=self.generate_new_dna_dir_name(self.config_['common']['dna_path'])
        if not os.path.exists(new_dna_dir):
            os.mkdir(new_dna_dir)
            info('New DNA dir does not exist, make dir: '+new_dna_dir)

        dest_dir = os.path.abspath(os.path.join(self.config_['common']['generated_dir']))
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        generator = PEGeneratorGa(self.config_)
        generator.load_sample(file_path)
        generator.load_dna()
        generator.set_dest_dir(dest_dir)
        #生成ga_new_generated_samples/PE文件夹
        generator.set_generated_dir(dest_dir)
        #产生ga_new_generated_samples/hcx_target_dir_文件夹
        generator.set_hcx_target_dir(dest_dir)


        generator.evolution(self.config_['pe_generator_ga']['count'])


    def attack(self):
        #print('> Begin to attack, index = {}'.format(index))
        #self.set_index(index)
        #
        sample_path = self.config_['common']['samples']
        if not os.path.exists(sample_path):
            raise Exception('Cannot find sample path: {}'.format(sample_path))

        self.process_file(sample_path)

    def generate_new_dna_dir_name(self,dna_dir_name):
        dna_dir_name = dna_dir_name.rstrip('\\/')
        if '_round_' in dna_dir_name:
            raw_dna_dir_name, round = dna_dir_name.split('_round_')
            return raw_dna_dir_name + '_round_' + str(int(round) + 1)
        else:
            return dna_dir_name + '_round_1'


if __name__ == '__main__':
    basicConfig(filename='adversary_ml_{}.log'.format(os.getpid()), format='[%(asctime)s][%(levelname)s] - %(message)s',
                level=INFO)
    with open('config_ga.json', 'r') as fh:
        config = json.load(fh)
    adv = AdversaryWorkflowGa(config)
    adv.attack()
