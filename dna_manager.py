import os
import random
from logging import *

class DNAManager:
    """"""

    def __init__(self):
        self.dna_code_list = []

    def get_dna(self):
        return self.dna_code_list

    def get_dna_random(self, count):
        list_len = len(self.dna_code_list)
        if list_len < count:
            raise Exception("Length of DNA is less than input count: {}".format(count))
        random_list = []
        for i in range(count):
            random_list.append(random.randint(0, list_len-1))
        # print(random_list)
        result = []
        for i in random_list:
            result.append(self.dna_code_list[i])
        return result

    def load_all_dna_files(self, dir_path):
        info('Load DNA files from {}'.format(dir_path))
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                with open(os.path.join(root, name), 'r') as fh:
                    content = fh.read()
                    self.dna_code_list.append(content)
        print("Load DNA files count: {}".format(len(self.dna_code_list)))

    def load_dna_files(self, dir_path, start, step):
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

    def save_dna_by_indexes(self, indexes, dir_path):
        index_list = [index for index, value in enumerate(indexes) if value == 1]
        for i in index_list:
            sha1 = hashlib.sha1(self.dna_code_list[i].encode('utf-8')).hexdigest()
            with open(os.path.join(dir_path, sha1), 'w') as fh:
                fh.write(self.dna_code_list[i])


