import os
import random
from logging import *


class DNAManager:
    """"""

    DNA_TYPE_SECTION = 0
    DNA_TYPE_IMPORTF = 1

    def __init__(self):
        self.dna_list_section = []
        self.dna_list_importf = []

    def get_dna(self, dna_type):
        if dna_type == DNAManager.DNA_TYPE_SECTION:
            return self.dna_list_section
        elif dna_type == DNAManager.DNA_TYPE_IMPORTF:
            return self.dna_list_importf
        else:
            return []

    def generate_random_indexes(self, count, list_len):
        if list_len < count:
            raise Exception("Length of DNA is less than input count: {}".format(count))
        random_indexes = []
        for i in range(count):
            random_indexes.append(random.randint(0, list_len-1))
        return random_indexes

    def get_dna_random(self, count, dna_type):
        list_len = len(self.dna_list_section)
        random_indexes = self.generate_random_indexes(count, list_len)
        result = []
        for i in random_indexes:
            if dna_type == DNAManager.DNA_TYPE_SECTION:
                result.append(self.dna_list_section[i])
            elif dna_type == DNAManager.DNA_TYPE_IMPORTF:
                result.append(self.dna_list_importf[i])
            else:
                pass
        return result

    def load_dna_files(self, dir_path, dna_type):
        info('Load DNA files from {}'.format(dir_path))
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                with open(os.path.join(root, name), 'r') as fh:
                    content = fh.read()
                    if dna_type == DNAManager.DNA_TYPE_SECTION:
                        self.dna_list_section.append(content)
                    elif dna_type == DNAManager.DNA_TYPE_IMPORTF:
                        self.dna_list_importf.append(content)
                    else:
                        pass
        print("[Load DNA Files] section count: {}, importf count: {}".format(len(self.dna_list_section), len(self.dna_list_importf)))

    def load_dna_files_partial(self, dir_path, start, step, dna_type):
        info('Load DNA files from {}, start = {}, step = {}, type = {}'.format(dir_path, start, step, dna_type))
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
                        if dna_type == DNAManager.DNA_TYPE_SECTION:
                            self.dna_list_section.append(content)
                        elif dna_type == DNAManager.DNA_TYPE_IMPORTF:
                            self.dna_list_importf.append(content)
                        else:
                            pass
                        append_count += 1
                index += 1

    def save_dna_by_indexes(self, indexes, dir_path, dna_type):
        index_list = [index for index, value in enumerate(indexes) if value == 1]
        for i in index_list:
            sha1 = hashlib.sha1(self.dna_list_section[i].encode('utf-8')).hexdigest()
            with open(os.path.join(dir_path, sha1), 'w') as fh:
                if dna_type == DNAManager.DNA_TYPE_SECTION:
                    fh.write(self.dna_list_section[i])
                elif dna_type == DNAManager.DNA_TYPE_IMPORTF:
                    fh.write(self.dna_list_importf[i])
                else:
                    pass


