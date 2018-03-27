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


def check_free_disk(disk_path):
    st = os.statvfs(disk_path)
    free = st.f_bavail * st.f_frsize
    free = free / 1024 / 1024 # convert to MB
    return free

class AdversaryWorkflow:
    """"""
    def __init__(self, config):
        self.config_ = config
        self.index_ = 1
        self.generate_count_ = 0

    def process_file(self, cpu_index,file_path):
        round = self.config_['pe_generator_random']['round']
        for i in range(round):
            print('CPU index: {}, Current round is {}'.format(cpu_index, i + 1))
            try:
                print('>> Attack {}'.format(file_path))
                #
                dest_dir = os.path.abspath(os.path.join(self.config_['common']['generated_dir'], str(os.getpid()), str(i)))
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                generator = PEGeneratorRandom(self.config_)
                generator.load_sample(file_path)
                generator.load_dna()
                generator.set_dest_dir(dest_dir)
                cur_count = self.config_['pe_generator_random']['count']
                generator.generate(cur_count)
                self.generate_count_ += cur_count
                #
                trendx = TrendXWrapper(self.config_)
                hcx_path = os.path.join('tools', 'housecallx', 'hcx{}'.format(cpu_index+1))
                trendx.set_hcx(hcx_path)
                scores = trendx.scan_pe_dir(dest_dir)
                
                for sample_path, value in scores.items():
                    if value[0] < 2:
                        if self.config_['cuckoo']['enable']:
                            try:
                                print("> Sample: {}, Decision: {}, Current Generated Sample Count: {}".format(sample_path,value[0],self.generate_count_))
                                info('Find non-malicious sample, decision is {}, submit to cuckoo sandbox: {}'.format(value[0], sample_path))
                                cmd = 'cuckoo submit --timeout 60 {}'.format(sample_path)
                                info('> ' + cmd)
                                print('> ' + cmd)
                                os.system(cmd)
                            except Exception as e:
                                print(e)
                    else:
                        os.remove(sample_path)
            except Exception as e:
                print(e)

            free = check_free_disk('/')
            if free < 1024:
                print('[*] CPU index: {}, No enough disk space, sleep 10 minutes!'.format(cpu_index))
                time.sleep(600)  # sleep 10m

    def process_dir(self, cpu_index, dir_path):
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                mal_sample_path = os.path.join(root, name)
                self.process_file(cpu_index, mal_sample_path)



    def attack(self, cpu_index):
        print('> Begin to attack, index = {}'.format(cpu_index))
        #
        sample_path = self.config_['common']['samples']
        if not os.path.exists(sample_path):
            raise Exception('Cannot find sample path: {}'.format(sample_path))
        if os.path.isdir(sample_path):
            self.process_dir(cpu_index,sample_path)
        elif os.path.isfile(sample_path):
            self.process_file(cpu_index,sample_path)


        else:
            pass

    def start(self):
        try:
            if self.config_['common']['use_cpu_count']:
                cpu_count = multiprocessing.cpu_count()
            else:
                cpu_count = 1
            # 
            p = NoDaemonPool(cpu_count)
            for i in range(cpu_count):
                p.apply_async(self.attack, args=(i,))
            p.close()
            p.join()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    basicConfig(filename='adversary_ml_{}.log'.format(os.getpid()), format='[%(asctime)s][%(process)d.%(thread)d][%(levelname)s] - %(message)s', level=INFO)
    with open('config.json', 'r') as fh:
        config = json.load(fh)
    adv = AdversaryWorkflow(config)
    adv.start()