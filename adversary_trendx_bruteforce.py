import os, sys, shutil
import time, json
from logging import *
import numpy as np
from logging import *
from pe_generator import *

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from trendx_wrapper import *

def check_free_disk(disk_path):
    st = os.statvfs(disk_path)
    free = st.f_bavail * st.f_frsize
    free = free / 1024 / 1024 # convert to MB
    return free

class TrendXBruteforceAdversary:
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
            
            #
            try:
                trendx = TrendXWrapper(self.config_)
                hcx_path = os.path.join('tools', 'housecallx', 'hcx{}'.format(cpu_index+1))
                trendx.set_hcx(hcx_path)
                scores = trendx.scan_pe_dir(dest_dir)
            except Exception as e:
                warn('Exception in trendx.scan_pe_dir, {}'.format(e))
                shutil.rmtree(dest_dir)
                return None

            for sample_path, value in scores.items():
                if value[0] < 2:
                    self.bypassed_count_ += 1
                    if self.config_['cuckoo']['enable'] and self.config_['cuckoo']['scan_in_file_proc']:
                        try:
                            print("> Sample: {}, Decision: {}, Current Generated Sample Count: {}".format(sample_path,value[0],self.generate_count_))
                            info('Find non-malicious sample, decision is {}, submit to cuckoo sandbox: {}'.format(value[0], sample_path))
                            cmd = 'cuckoo submit --timeout 60 {}'.format(sample_path)
                            info('> ' + cmd)
                            print('> ' + cmd)
                            os.system(cmd)
                        except Exception as e:
                            warn('Exception in cuckoo sandbox, {}'.format(e))
                            return None
                else:
                    if self.config_['common']['remove_not_bypassed']:
                        os.remove(sample_path)

        free = check_free_disk('/')
        if free < self.config_['common']['free_disk']:
            print('[*] CPU index: {}, No enough disk space, sleep 10 minutes!'.format(cpu_index))
            time.sleep(600)  # sleep 10m
        
        return (self.generate_count_, self.bypassed_count_)