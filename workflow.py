import os, sys
import time, json
from logging import *
from multiprocessing import Process, pool
from pe_generator_random import *
from tools.trendx_wrapper import *

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class NoDaemonPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


class AdversaryWorkflow:
    """"""
    def __init__(self, config):
        self.config_ = config
        self.index_ = 1

    def set_index(self, index):
        self.index_ = index

    def process_file(self, file_path):
        # 
        dest_dir = os.path.abspath(os.path.join(self.config_['common']['generated_dir'], str(os.getpid())))
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        generator = PEGeneratorRandom(self.config_)
        generator.load_sample(file_path)
        generator.load_dna()
        generator.set_dest_dir(dest_dir)
        generator.generate(self.config_['pe_generator_random']['count'])
        # 
        trendx = TrendXWrapper(self.config_)
        hcx_path = os.path.join('tools', 'housecallx', 'hcx{}'.format(self.index_))
        trendx.set_hcx(hcx_path)
        scores = trendx.scan_pe_dir(dest_dir)
        for sample_path, value in scores.items():
            if value[0] < 2:
                try:
                    print("> Sample: {}, Decision: {}".format(sample_path,value[0]))
                    info('Find non-malicious sample, decision is {}, submit to cuckoo sandbox: {}'.format(value[0], sample_path))
                    cmd = 'cuckoo submit --timeout 60 {}'.format(sample_path)
                    info('> ' + cmd)
                    print('> ' + cmd)
                    os.system(cmd)
                except Exception as e:
                    print(e)
            else:
                os.remove(sample_path)
    
    def process_dir(self, dir_path):
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                for i in range(self.config_['pe_generator_random']['round']):
                    self.process_file(os.path.join(root, name))

    def attack(self, index):
        print('> Begin to attack, index = {}'.format(index))
        self.set_index(index)
        #
        sample_path = self.config_['common']['samples']
        if not os.path.exists(sample_path):
            raise Exception('Cannot find sample path: {}'.format(sample_path))
        if os.path.isdir(sample_path):
            self.process_dir(sample_path)
        elif os.path.isfile(sample_path):
            self.process_file(sample_path)
        else:
            pass

    def start(self):
        try:
            cpu_count = multiprocessing.cpu_count()
            # 
            p = NoDaemonPool(cpu_count)
            for i in range(cpu_count):
                p.apply_async(self.attack, args=(i,))
            p.close()
            p.join()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    basicConfig(filename='adversary_ml_{}.log'.format(os.getpid()), format='[%(asctime)s][%(levelname)s] - %(message)s', level=INFO)
    with open('config.json', 'r') as fh:
        config = json.load(fh)
    adv = AdversaryWorkflow(config)
    adv.start()