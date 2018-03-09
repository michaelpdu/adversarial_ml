import os, sys, shutil
import numpy as np
import hashlib
from datetime import datetime
import random
from logging import *

sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from trendx_tool.run import *
from pe_modifier.pe_modifier import *
from housecallx_wrapper import *


class TrendxAdversary:
    """"""

    SCAN_TYPE_SCRIPT = 0
    SCAN_TYPE_BINARY = 1

    def __init__(self):
        self.scan_type = TrendxAdversary.SCAN_TYPE_BINARY
        self.mal_file_path = ''
        self.dna_code_list = []
        self.tmp_file_dir = os.path.abspath('tmp_file_dir')
        self.new_generated_file = 'new_generated_file.tmp'
        self.housecallx_path = 'housecallx'
        self.new_generated_dir = 'new_generated_files'
        self.hcx_target_dir = os.path.join(self.new_generated_dir, 'hcx_target_dir')

    def set_housecallx_path(self, housecallx):
        info('Set HouseCallX: {}'.format(housecallx))
        self.housecallx_path = housecallx

    def set_scan_type(self, scan_type):
        info('Set scan type: {}'.format(scan_type))
        self.scan_type = scan_type

    def set_malicious_file(self, file_path):
        info('Set file path: {}'.format(file_path))
        self.mal_file_path = file_path
        dir_path, file_name = os.path.split(file_path)
        name_wo_ext, ext = os.path.splitext(file_name)
        self.mal_file_name_wo_ext = name_wo_ext

    def set_generated_file_name(self, name):
        self.new_generated_file = os.path.join(self.tmp_file_dir, name)
        info('Set new generated file: {}'.format(self.new_generated_file))

    def set_generated_dir(self, dir_path):
        info('Set new generated dir: {}'.format(dir_path))
        self.new_generated_dir = dir_path

    def set_hcx_target_dir(self, dir_path):
        info('Set HouseCallX target dir: {}'.format(dir_path))
        self.hcx_target_dir = dir_path

    def save_dna_by_indexes(self, dir_path, indexes):
        index_list = [index for index, value in enumerate(indexes) if value == 1]
        for i in index_list:
            sha1 = hashlib.sha1(self.dna_code_list[i].encode('utf-8')).hexdigest()
            with open(os.path.join(dir_path, sha1), 'w') as fh:
                fh.write(self.dna_code_list[i])

    def save_new_sample_with_dna(self, file_path, indexes):
        info('Save new sample to {} by DNA: {}'.format(file_path, indexes))
        index_list = [index for index, value in enumerate(indexes) if value == 1]
        with open(file_path, 'w') as fh:
            fh.write(self.generate_new_script(index_list))

    # read function code
    def load_dna_files(self, dir_path, start = 0, step = 32):
        info('Load DNA files from {}, start = {}, step = {}'.format(dir_path, start, step))
        start_index = start
        step_len = step
        index = 0
        append_count = 0
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                if append_count >= step:
                    break
                if start_index <= index:
                    with open(os.path.join(root, name), 'r') as fh:
                        content = fh.read()
                        self.dna_code_list.append(content)
                        append_count += 1
                index += 1

    # generate new content according to DNA
    def generate_new_script(self, index_list):
        debug('Generate new script by {}'.format(index_list))
        mal_script_content = ''
        with open(self.mal_file_path, 'r') as fh:
            mal_script_content = fh.read()
        new_mal_content = mal_script_content
        for i in index_list:
            new_mal_content += '\n\n'
            new_mal_content += self.dna_code_list[i]
        return new_mal_content

    def calc_script_prediction(self, dna_array):
        debug('Calculate script prediction')
        dna_list = dna_array.tolist()
        prob_list = []
        for dna in dna_list:
            # print item
            indexes = [index for index, value in enumerate(dna) if value == 1]
            # print '>> '+str(indexes)
            # for JavaScript
            new_content = self.generate_new_script(indexes)
            debug('Save generated file into {}'.format(self.new_generated_file))
            with open(self.new_generated_file, 'w') as fh:
                fh.write(new_content)
            # use trendx_tool to scan new sample
            m = JSModel()
            prob = m.predictfile(self.new_generated_file)
            debug('Predict file: {}, and probability: {}'.format(self.new_generated_file, prob))
            prob_list.append(1-prob)
        ret_array = np.array(prob_list)
        ret_val = ret_array[:,0]
        # return type is ndarray, and shape is (dna_size,)
        return ret_val

    def generate_new_pe(self, index_list):
        modifier = PEModifier()
        modifier.load_pe(self.mal_file_path)
        section_add_list = []
        imports_append_list = []

        for i in index_list:
            lines = self.dna_code_list[i].strip().split('\n')
            cmd = lines[0]
            if cmd == 'section_add':
                # section content
                str_list = lines[1].split(' ')
                int_list = []
                for s in str_list:
                    int_list.append(int(s))
                section_add_list.append(int_list)
            elif cmd == 'imports_append':
                dllname = lines[1]
                funcname = lines[2]
                imports_append_list.append((dllname, funcname))
            else:
                pass
        if len(section_add_list) > 0:
            modifier.modify({'section_add_list': section_add_list})
        elif len(imports_append_list) > 0:
            modifier.modify({'imports_append_list': imports_append_list})
        else:
            pass
        # save new generated file into hcx_target_dir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        tmp_file = '{}_new_generated_file_{}.tmp'.format(self.mal_file_name_wo_ext, timestamp)
        new_pe_path = os.path.join(self.hcx_target_dir, tmp_file)
        modifier.save_pe(new_pe_path)
        return new_pe_path

    def calc_binary_prediction(self, dna_array):
        dna_list = dna_array.tolist()
        prob_list = []
        dna_pe_map = {}

        # empty hcx_target_dir
        if os.path.exists(self.hcx_target_dir):
            shutil.rmtree(self.hcx_target_dir)
        os.makedirs(self.hcx_target_dir)

        print('Generate new PE files ....')
        for dna in dna_list:
            # print item
            indexes = [index for index, value in enumerate(dna) if value == 1]
            # calc sha1 for indexs
            sha1_value = hashlib.sha1()
            for i in indexes:
                sha1_value.update(str(i).encode('utf-8'))
            sha1_str = sha1_value.hexdigest()

            # print '>> '+str(indexes)
            new_pe_path = self.generate_new_pe(indexes)
            dna_pe_map[sha1_str] = os.path.split(new_pe_path)[1]

        # use housecallx to scan new pe
        scores = scan_by_housecallx(self.housecallx_path, os.path.abspath(self.hcx_target_dir))

        # for file_name, score in scores.items():
        #     print('File Name: {}, Score: {}'.format(file_name, score))

        # build dna_hash --> score
        dna_hash_scores = {}
        for dna_hash, file_name in dna_pe_map.items():
            dna_hash_scores[dna_hash] = scores[file_name]

        # append scores according to dna_hash
        for dna in dna_list:
            # print item
            indexes = [index for index, value in enumerate(dna) if value == 1]
            # calc sha1 for indexs
            sha1_value = hashlib.sha1()
            for i in indexes:
                sha1_value.update(str(i).encode('utf-8'))
            sha1_str = sha1_value.hexdigest()
            prob_list.append(dna_hash_scores[sha1_str])

        # move all of files in hc_target_dir to 
        for file in os.listdir(self.hcx_target_dir):
            if not os.path.exists(os.path.join(self.new_generated_dir,file)):
                shutil.move(os.path.join(self.hcx_target_dir, file), self.new_generated_dir)
        for file_name, score in scores.items():
            # print('File: {}, Score: {}'.format(file_name, score))
            if int(score) > 100:
                cmd = 'cuckoo submit --timeout 60 {}'.format(os.path.join(self.new_generated_dir, file_name))
                info('Find non-normal sample, score is {}, cmd: {}'.format(score, cmd))
                os.system(cmd)
                

        ret_array = np.array(prob_list)
        # return type is ndarray, and shape is (dna_size,)
        return ret_array

    def generate_new_pe_random(self, action_id = 0, times = 100):
        modifier = PEModifier()
        modifier.load_pe(self.mal_file_path)

        action_list = ['overlay_append',
                        'imports_append',
                        'section_rename',
                        'section_add',
                        'section_append',
                        'create_new_entry',
                        'remove_signature',
                        'remove_debug',
                        'upx_pack',
                        'upx_unpack',
                        'break_optional_header_checksum']
        action_id = action_id % len(action_list)
        action = action_list[action_id]

        for i in range(0,times):
            modifier.modify({action: None})
            
        # save new generated file into hcx_target_dir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        tmp_file = '{}_new_generated_file_{}_{}.tmp'.format(self.mal_file_name_wo_ext, action, timestamp)
        new_pe_path = os.path.join(self.hcx_target_dir, tmp_file)
        modifier.save_pe(new_pe_path)
        return new_pe_path

    def calc_binary_prediction_random(self, action_id_list):
        # empty hcx_target_dir
        if os.path.exists(self.hcx_target_dir):
            shutil.rmtree(self.hcx_target_dir)
        os.makedirs(self.hcx_target_dir)

        print('Generate new PE files ....')
        for action_id in action_id_list:
            new_pe_path = self.generate_new_pe_random(action_id, 5)

        # use housecallx to scan new pe
        scores = scan_by_housecallx(self.housecallx_path, os.path.abspath(self.hcx_target_dir))

        # move all of files in hc_target_dir to 
        for file in os.listdir(self.hcx_target_dir):
            if not os.path.exists(os.path.join(self.hcx_target_dir,file)):
                shutil.move(os.path.join(self.hcx_target_dir, file), self.new_generated_dir)

    def calc_trendx_prediction(self, dna_array):
        # 
        if not os.path.exists(self.new_generated_dir):
            os.makedirs(self.new_generated_dir)
        #
        if self.scan_type == TrendxAdversary.SCAN_TYPE_SCRIPT:
            return self.calc_script_prediction(dna_array)
        elif self.scan_type == TrendxAdversary.SCAN_TYPE_BINARY:
            if not os.path.exists(self.hcx_target_dir):
                os.makedirs(self.hcx_target_dir)
            return self.calc_binary_prediction(dna_array)
        else:
            return 0

help_msg = """
Usage:
    >> python tool.py malicious_pe_file housecallx_dir
"""

if __name__ == '__main__':
    # step = 32
    # adv = TrendxAdversary()
    # adv.load_dna_files(r'function_snippet', 0, step)
    # random_dna = np.random.randint(2, size=(200, step))
    # print(adv.calc_trendx_prediction(random_dna))
    adv = TrendxAdversary()
    adv.set_malicious_file(sys.argv[1])
    new_generated_dir = 'new_generated_files'
    adv.set_generated_dir(os.path.join(new_generated_dir, 'PE'))
    adv.set_hcx_target_dir(os.path.join(new_generated_dir, 'hcx_target_dir_{}'.format(os.getpid())))
    adv.set_housecallx_path(sys.argv[2])
    action_id_list = [3]
    # for i in range(0,5):
    #     action_id_list += random.sample([1,3,4,5,6,7,10], 5)
    adv.calc_binary_prediction_random(action_id_list)
