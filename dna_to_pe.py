import lief
import os
import sys
import numpy as np
from optparse import OptionParser
from logging import *
import hashlib
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from pe_modifier.pe_modifier import *
from datetime import datetime


def make_new_pe(mal_sample_file, current_dna_dir, start_index,dna_size,pe_num):



    # set malicious content and new generated folder to adversary

    mal_file_name=set_malicious_file(mal_sample_file)
    new_generated_dir = 'new_generated_pe_files'
    timestamp = datetime.now().strftime("%Y%m%d")
    mal_file_name_path=mal_file_name+"_"+timestamp+"_"+str(pe_num)
    new_generated_dir=os.path.join(new_generated_dir,mal_file_name_path)
    if not os.path.exists(new_generated_dir):
        os.makedirs(new_generated_dir)
    #print("----------------------"+mal_file_name)
    #print("----------------------"+mal_file_name_wo_ext)
    #print(new_generated_dir)
    POP_SIZE=pe_num
    DNA_SIZE=dna_size
    pop = np.random.randint(2, size=(POP_SIZE,DNA_SIZE))
    dna_code_list=load_dna_files(current_dna_dir, start_index, dna_size)
    print('Generate new PE files ....')
    calc_binary_prediction(pop,mal_sample_file,dna_code_list,mal_file_name,new_generated_dir)


    # if type == TrendxAdversary.SCAN_TYPE_SCRIPT:
    #     adv.save_new_sample_with_dna('{}_most'.format(tmp_file),most_valuable_dna)
    #     os.remove(tmp_file)

    # save good DNA in next round DNA directory
    #adv.save_dna_by_indexes(new_dna_dir, most_valuable_dna)



def set_malicious_file(file_path):
    info('Set file path: {}'.format(file_path))
    mal_file_path = file_path
    dir_path, file_name = os.path.split(file_path)


    return file_name

def set_generated_dir(dir_path):
    info('Set new generated dir: {}'.format(dir_path))
    new_generated_dir = dir_path

def load_dna_files(dir_path, start = 0, step = 32):
    info('Load DNA files from {}, start = {}, step = {}'.format(dir_path, start, step ))

    start_index = start
    step_len = step
    index = 0
    append_count = 0
    dna_code_list=[]
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            if append_count >= step:
                break
            if start_index <= index:
                with open(os.path.join(root, name), 'r') as fh:
                    content = fh.read()
                    dna_code_list.append(content)
                    append_count += 1
            index += 1
    return dna_code_list

def calc_binary_prediction(dna_array,mal_sample_file,dna_code_list,mal_file_name,new_generated_dir):
    dna_list = dna_array.tolist()
    for dna in dna_list:
        # print item
        indexes = [index for index, value in enumerate(dna) if value == 1]
        # calc sha1 for indexs
        sha1_value = hashlib.sha1()
        for i in indexes:
            sha1_value.update(str(i).encode('utf-8'))
        sha1_str = sha1_value.hexdigest()
        generate_new_pe(indexes,mal_sample_file,dna_code_list,mal_file_name,new_generated_dir)

def generate_new_pe(index_list,mal_sample_file,dna_code_list,mal_file_name,new_generated_dir):
    try:
        modifier = PEModifier()
        modifier.load_pe(mal_sample_file)
        section_add_list = []
        imports_append_list = []
        cur_len = len(dna_code_list)
        # print("Length of DNA code list: {}".format(cur_len))
        # print(index_list)
        for i in index_list:
            if i >= cur_len:
                continue
            lines = dna_code_list[i].strip().split('\n')
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
        print("长度为"+str(len(section_add_list)))
        if len(section_add_list) > 0:
            modifier.modify({'section_add_list': section_add_list})
        elif len(imports_append_list) > 0:
            modifier.modify({'imports_append_list': imports_append_list})
        else:
            pass
        #code.interact(local=locals())
        # save new generated file into hcx_target_dir
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        tmp_file = '{}_{}_{}'.format(mal_file_name, timestamp, modifier.get_hash_sha1())
        #print(new_generated_dir)
        #print(tmp_file)
        new_pe_path = os.path.join(new_generated_dir,tmp_file)
        #print(new_pe_path+"=======================")
        modifier.save_pe(new_pe_path)
        #print("保存成功")
        #return new_pe_path
    except Exception as e:
        print('[generate_new_pe] {}'.format(e))

help_msg = """
Usage:
    
    (a) from DNA to PE
        
        >> python3  dna_to_pe.py --file-type PE --file-path malicious_pe --dna DNA_dir --step DNA_size --pe-num new_pe_number
        e.g.
        >> python3 dna_to_pe.py --file-type PE --file-path samples/mal_pe/6d3e5e56984a7e91c7a8c434224b73886d413d1d1f435358f40bf78c71c1932d --dna DNA/DNA_PE/section_add --step 32 --pe-num 100
"""












if __name__ == '__main__':
    parser = OptionParser(usage=help_msg)
    parser.add_option("--file-type", dest="file_type",
                      help="specify file type", metavar="FILE-TYPE")
    parser.add_option("--file-path", dest="file_path",
                      help="specify malicious file path", metavar="FILE-PATH")
    parser.add_option("--dna", dest="dna_path",
                      help="specify DNA path", metavar="DNA-PATH")
    parser.add_option("--start", dest="start_index",
                      help="specify start index", metavar="START-INDEX")
    parser.add_option("--step", dest="step",
                      help="specify step", metavar="STEP")
    parser.add_option("--pe-num", dest="pe_num",
                      help="specify PE number", metavar="PE_NUM")


    (options, args) = parser.parse_args()
    # set config in logging
    #basicConfig(filename='adversary_ml_{}.log'.format(os.getpid()), format='[%(asctime)s][%(levelname)s] - %(message)s', level=INFO)

    if options.file_type:
        if not os.path.exists(options.file_path):
            print('Cannot find {}'.format(options.file_path))
            exit(-1)
        if not os.path.exists(options.dna_path):
            print('Cannot find {}'.format(options.dna_path))
            exit(-1)
        info('Type: {}, Malicious File: {}, DNA: {}, Start Index: {}, Step: {}, Num: {}'.format(options.file_type,
                                                                                       options.file_path,
                                                                                       options.dna_path,
                                                                                       options.start_index,
                                                                                       options.step
                                                                                       ,options.pe_num))
        if options.file_type == 'PE':
            make_new_pe(options.file_path, options.dna_path,int(options.start_index),int(options.step),int(options.pe_num))
    else:
        print(help_msg)