import os, sys, shutil
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
        self.bypassed_count_ = 0
        self.generator_ = PEGeneratorRandom(self.config_)
        self.generator_.load_dna()

    def process_file(self, cpu_index, file_path):
        try:
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
                self.generator_.generate(cur_count)
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
                    else:
                        if self.config_['common']['remove_not_bypassed']:
                            os.remove(sample_path)

            free = check_free_disk('/')
            if free < self.config_['common']['free_disk']:
                print('[*] CPU index: {}, No enough disk space, sleep 10 minutes!'.format(cpu_index))
                time.sleep(600)  # sleep 10m
        except Exception as e:
            warn('Exception in workflow.process_file, {}'.format(e))

    def process_dir(self, cpu_index, dir_path):
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                mal_sample_path = os.path.join(root, name)
                self.process_file(cpu_index, mal_sample_path)

    def process(self, cpu_index):
        sample_path = self.config_['common']['samples']
        if not os.path.exists(sample_path):
            raise Exception('Cannot find sample path: {}'.format(sample_path))
        if os.path.isdir(sample_path):
            self.process_dir(cpu_index,sample_path)
        elif os.path.isfile(sample_path):
            self.process_file(cpu_index,sample_path)
        else:
            pass
        
        #
        if self.config_['cuckoo']['enable'] and (not self.config_['cuckoo']['scan_in_file_proc']):
            try:
                cmd = 'cuckoo submit --timeout 60 {}'.format(os.path.abspath(self.config_['common']['generated_dir']))
                info('> ' + cmd)
                print('> ' + cmd)
                os.system(cmd)
            except Exception as e:
                warn('Exception in cuckoo sandbox, {}'.format(e))

        return (self.generate_count_, self.bypassed_count_)

def start(cpu_index, config):
    adv = AdversaryWorkflow(config)
    print('> Begin to attack, index = {}'.format(cpu_index))
    return adv.process(cpu_index)

def attack(config):
    try:
        results = []
        def attack_callback(result):
            results.append(result)

        cpu_count = config['common']['use_cpu_count']
        if config['common']['enable_system_cpu']:
            cpu_count = multiprocessing.cpu_count()

        # 
        p = NoDaemonPool(cpu_count)
        for i in range(cpu_count):
            p.apply_async(start, args=(i, config), callback=attack_callback)
        p.close()
        p.join()

        # show statistic info
        total_gen = 0
        total_bypassed = 0

        for result in results:
            total_gen += result[0]
            total_bypassed += result[1]
        msg = '[*] Total generated: {}, total bypassed: {}'.format(total_gen, total_bypassed)
        info(msg)
        print(msg)
        
        return (total_gen, total_bypassed)
    except Exception as e:
        warn('Exception in attack, {}'.format(e))


if __name__ == '__main__':
    basicConfig(filename='adversary_ml_{}.log'.format(os.getpid()), format='[%(asctime)s][%(process)d.%(thread)d][%(levelname)s] - %(message)s', level=INFO)
    with open('config.json', 'r') as fh:
        config = json.load(fh)
    attack(config)
