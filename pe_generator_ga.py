import os,sys,shutil
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from pe_modifier.pe_modifier import *
from housecallx_wrapper import *
import numpy as np
import hashlib
from datetime import datetime
import random
from logging import *
import code

class PEGeneratorGa:
    SCAN_TYPE_SCRIPT = 0
    SCAN_TYPE_BINARY = 1

    def __init__(self, config):
        self.config_ = config
        self.dna_code_list = []
        self.housecallx_path=self.config_["trendx"]["housecallx"]
        self.POP_SIZE=int(self.config_["pe_generator_ga"]["count"])
        self.DNA_SIZE=int(self.config_["common"]["step"])
        self.CROSS_RATE=int(self.config_["ga_param"]["cross_rate"])
        self.MUTATION_RATE=int(self.config_["ga_param"]["mutation_rate"])

    def load_sample(self, sample_path):
        self.modifier_ = PEModifier()
        self.modifier_.load_pe(sample_path)
        dir_path, filename = os.path.split(sample_path)
        self.mal_file_path=sample_path
        self.mal_file_name_wo_ext, ext = os.path.splitext(filename)

    def load_dna(self):
        #self.dna_mgr_ = DNAManagerGa(self.config_)
        self.load_dna_files(self.config_["common"]["dna_path"],self.config_["common"]["start"],self.config_["common"]["step"])

    def load_dna_files(self, dir_path, start = 0, step = 32):
        info('Load DNA files from {}, start = {}, step = {}'.format(dir_path, start, step))
        start_index = start
        step_len = step
        index = 0
        append_count = 0
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                if append_count >= int(step):
                    break
                if int(start_index) <= index:
                    with open(os.path.join(root, name), 'r') as fh:
                        content = fh.read()
                        self.dna_code_list.append(content)
                        append_count += 1
                index += 1

    def set_dest_dir(self, dest_dir):
        self.dest_dir_ = dest_dir
        if not os.path.exists(self.dest_dir_):
            os.makedirs(self.dest_dir_)

    def set_generated_dir(self, dir_path):
        dir_path=os.path.join(dir_path, 'PE')
        info('Set new generated dir: {}'.format(dir_path))
        self.new_generated_dir = dir_path
    #产生
    def set_hcx_target_dir(self, dir_path):
        dir_path=os.path.join(dir_path, 'hcx_target_dir_{}'.format(os.getpid()))
        info('Set HouseCallX target dir: {}'.format(dir_path))
        self.hcx_target_dir = dir_path



#--------------遗传算法部分----------------
    def evolution(self,count):
        count=int(count)
        pop = np.random.randint(2,size=(count,int(self.config_["common"]["step"])))  # initialize the pop DNA
        max_value = 0
        most_dna = []
        for _ in range(self.config_["pe_generator_ga"]["round"]):
            F_values = self.calc_trendx_prediction(pop)
            fitness = self.get_fitness(F_values)
            dna = pop[np.argmax(fitness), :]
            value = F_values[np.argmax(fitness)]
            msg = "G{}: Most fitted DNA: {}, and value: {}".format(_, dna, value)
            info(msg)
            print(msg)
            if max_value < value:
                max_value = value
                most_dna = dna.tolist()
            pop = self.select(pop, fitness)
            pop_copy = pop.copy()
            for parent in pop:
                child = self.crossover(parent, pop_copy)
                child = self.mutate(child)
                parent[:] = child  # parent is replaced by its child
        return (most_dna, max_value)

    def calc_trendx_prediction(self, dna_array):
        #
        if not os.path.exists(self.new_generated_dir):
            os.makedirs(self.new_generated_dir)

        if self.config_["trendx"]["scan_type"] == PEGeneratorGa.SCAN_TYPE_BINARY:
            if not os.path.exists(self.hcx_target_dir):
                os.makedirs(self.hcx_target_dir)
            return self.calc_binary_prediction(dna_array)
        else:
            return 0

    def calc_binary_prediction(self, dna_array):
        dna_list = dna_array.tolist()
        prob_list = []
        dna_pe_map = {}
        pe_dna_map = {}

        # empty hcx_target_dir
        if os.path.exists(self.hcx_target_dir):
            shutil.rmtree(self.hcx_target_dir)
        os.makedirs(self.hcx_target_dir)

        print('Generate new PE files ....')
        # 产生100个新的PE文件
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
            pe_name = os.path.split(new_pe_path)[1]
            dna_pe_map[sha1_str] = pe_name
            pe_dna_map[pe_name] = dna

        # use housecallx to scan new pe
        # scores is a map object
        # {file_name: score}
        scores = scan_by_housecallx(self.housecallx_path, os.path.abspath(self.hcx_target_dir), pe_dna_map)

        # for file_name, score in scores.items():
        #     info('File Name: {}, Score: {}'.format(file_name, score))

        # backup all of non-malicious samples and scan in cuckoo sandbox

        for file_name, score in scores.items():
            ori_file_path = os.path.join(self.hcx_target_dir, file_name)
            file_path = os.path.join(self.new_generated_dir, file_name)
            # print('File: {}, Score: {}'.format(file_name, score))
            if int(score) >= 100:
                if os.path.exists(file_path):
                    os.remove(file_path)

                shutil.move(ori_file_path, self.new_generated_dir)
                print(file_name, '==========', score)

                # info('Find non-malicious sample, score is {}, submit to cuckoo sandbox: {}'.format(score, cmd))
                # cmd = 'cuckoo submit --timeout 60 {}'.format(file_path)
                # os.system(cmd)

        # remove temp dir
        # if os.path.exists(self.hcx_target_dir):
        #     shutil.rmtree(self.hcx_target_dir)



        # build dna_hash --> score
        # {dna_hash: score}
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

        ret_array = np.array(prob_list)
        # return type is ndarray, and shape is (dna_size,)
        return ret_array


    def generate_new_pe(self, index_list):
        try:
            modifier = PEModifier()
            modifier.load_pe(self.mal_file_path)
            section_add_list = []
            imports_append_list = []
            cur_len = len(self.dna_code_list)
            # print("Length of DNA code list: {}".format(cur_len))
            # print(index_list)
            for i in index_list:
                if i >= cur_len:
                    continue
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
            #code.interact(local=locals())
            # save new generated file into hcx_target_dir
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            tmp_file = '{}_{}_{}'.format(self.mal_file_name_wo_ext, timestamp, modifier.get_hash_sha1())
            new_pe_path = os.path.join(self.hcx_target_dir, tmp_file)
            modifier.save_pe(new_pe_path)
            return new_pe_path
        except Exception as e:
            print('[generate_new_pe] {}'.format(e))

    def get_fitness(self, pred):
        return pred + 1e-3 - np.min(pred)

    def select(self, pop, fitness):    # nature selection wrt pop's fitness
        idx = np.random.choice(np.arange(self.POP_SIZE), size=self.POP_SIZE, replace=True,
                               p=fitness/fitness.sum())
        return pop[idx]

    def crossover(self, parent, pop):     # mating process (genes crossover)
        if np.random.rand() < self.CROSS_RATE:
            i_ = np.random.randint(0, self.POP_SIZE, size=1)                             # select another individual from pop
            cross_points = np.random.randint(0, 2, size=self.DNA_SIZE).astype(np.bool)   # choose crossover points
            parent[cross_points] = pop[i_, cross_points]                            # mating and produce one child
        return parent

    def mutate(self, child):
        for point in range(self.DNA_SIZE):
            if np.random.rand() < self.MUTATION_RATE:
                child[point] = 1 if child[point] == 0 else 0
        return child























