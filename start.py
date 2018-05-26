import os, sys, shutil
import time, json
from logging import *
import multiprocessing
from multiprocessing import Process, pool

from adversary_tlsh_ga import TLSHGAAdversary
from adversary_tlsh_bruteforce import TLSHBruteforceAdversary
# from adversary_trendx_ga import *
from adversary_trendx_bruteforce import TrendXBruteforceAdversary
from genetic_algorithm_basic import GeneticAlgorithmHelper

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
        self.generated_count_ = 0
        self.bypassed_count_ = 0

    def process_file_in_trendx_pe_brute_force(self, cpu_index, file_path):
        # try:
        trendx_adv = TrendXBruteforceAdversary(self.config_)
        return trendx_adv.process_random(cpu_index, file_path)
        # except Exception as e:
        #     error('Exception in workflow.process_file_in_trendx_pe_brute_force, {}'.format(e))

    def process_file_in_trendx_pe_ga(self, cpu_index, file_path):
        pass

    def process_file_in_tlsh_pe_brute_force(self, cpu_index, file_path):
        tlsh_adv = TLSHBruteforceAdversary(self.config_)
        return tlsh_adv.process_random(cpu_index, file_path)

    def process_file_in_tlsh_pe_ga(self, cpu_index, file_path):
        # try:
        self.config_['tlsh']['scan_type'] = TLSHGAAdversary.SCAN_TYPE_BINARY
        adv = TLSHGAAdversary(self.config_)
        adv.set_malicious_file(file_path)
        # prepare algrithm helper and set DNA size in each group
        helper = GeneticAlgorithmHelper(self.config_['genetic_algorithm'])
        helper.set_adv(adv)
        helper.set_calc_callback(adv.calc_tlsh)
        helper.set_msg_callback(adv.display_message)
        # evolution
        most_valuable_dna, max_value = helper.evolution()
        print('*** In this evolution, most valuable DNA: {}, maximium value: {}'.format(str(most_valuable_dna), max_value))
        # print(adv.get_sample_info())
        return adv.get_sample_info()
        # except Exception as e:
        #     error('Exception in workflow.process_file_in_tlsh_pe_ga, {}'.format(e))

    def process_file(self, cpu_index, file_path):
        algorithm = self.config_['common']['algorithm']
        target = self.config_['common']['target']
        if algorithm == 'ga':
            if target == 'tlsh_pe':
                self.generated_count_, self.bypassed_count_ = self.process_file_in_tlsh_pe_ga(cpu_index, file_path)
            else:
                print('ERROR: Unsupported target name in GA')
        elif algorithm == 'bruteforce':
            if target == 'tlsh_pe':
                self.generated_count_, self.bypassed_count_ = self.process_file_in_tlsh_pe_brute_force(cpu_index, file_path)
            elif target == 'trendx_pe':
                self.generated_count_, self.bypassed_count_ = self.process_file_in_trendx_pe_brute_force(cpu_index, file_path)
            else:
                print('ERROR: Unsupported target name in Bruteforce')
        else:
            print("ERROR: Unsupported algorithm!")

    def process_dir(self, cpu_index, dir_path):
        total_generated_count = 0
        total_bypassed_count = 0
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                mal_sample_path = os.path.join(root, name)
                self.process_file(cpu_index, mal_sample_path)
                total_generated_count += self.generated_count_
                total_bypassed_count += self.bypassed_count_
        self.generated_count_ = total_generated_count
        self.bypassed_count_ = total_bypassed_count

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

        return (self.generated_count_, self.bypassed_count_)

def start(cpu_index, config):
    # try:
    adv = AdversaryWorkflow(config)
    print('> Begin to attack, index = {}'.format(cpu_index))
    return adv.process(cpu_index)
    # except Exception as e:
    #     print(e)
    #     return None

def attack(config):
    # try:
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
        if result is not None:
            total_gen += result[0]
            total_bypassed += result[1]
    msg = '[*] Total generated: {}, total bypassed: {}'.format(total_gen, total_bypassed)
    info(msg)
    print(msg)
    
    return (total_gen, total_bypassed)
    # except Exception as e:
    #     warn('Exception in attack, {}'.format(e))


if __name__ == '__main__':
    basicConfig(filename='adversary_ml_{}.log'.format(os.getpid()), format='[%(asctime)s][%(process)d.%(thread)d][%(levelname)s] - %(message)s', level=INFO)
    with open('config.json', 'r') as fh:
        config = json.load(fh)
    attack(config)
