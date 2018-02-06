import os, sys
import time
from calc_trendx_prediction import *
from genetic_algorithm_basic import *
from optparse import OptionParser
from logging import *


# what's one group?
#
def process_one_group(type, mal_sample_file, current_dna_dir, new_dna_dir, start_index, dna_size, housecallx_dir = ''):
    # check if new_dna_dir exists or not?
    if not os.path.exists(new_dna_dir):
        os.mkdir(new_dna_dir)
        info('New DNA dir does not exist, make dir: '+new_dna_dir)
    # set malicious content and new generated folder to adversary
    adv = TrendxAdversary()
    adv.set_malicious_file(mal_sample_file)
    new_generated_dir = 'new_generated_files'
    adv.set_scan_type(type)
    if type == TrendxAdversary.SCAN_TYPE_BINARY:
        adv.set_generated_dir(os.path.join(new_generated_dir, 'PE'))
        adv.set_hcx_target_dir(os.path.join(new_generated_dir, 'hcx_target_dir_{}'.format(os.getpid())))
        adv.set_housecallx_path(housecallx_dir)
    else:
        adv.set_generated_dir(os.path.join(new_generated_dir, 'JS'))

    # prepare algrithm helper and set DNA size in each group
    helper = GeneticAlgorithmHelper(adv)
    helper.set_dna_size(dna_size)
    # prepare DNA snippet
    adv.load_dna_files(current_dna_dir, start_index, dna_size)
    # evolution
    most_valuable_dna, max_value = helper.evolution()
    print('*** In this evolution, most valuable DNA: {}, maximium value: {}'.format(str(most_valuable_dna), max_value))

    # if type == TrendxAdversary.SCAN_TYPE_SCRIPT:
    #     adv.save_new_sample_with_dna('{}_most'.format(tmp_file),most_valuable_dna)
    #     os.remove(tmp_file)

    # save good DNA in next round DNA directory
    adv.save_dna_by_indexes(new_dna_dir, most_valuable_dna)

#
# Ori DNA(Depth 0): (00101101000100001101011100010111)(00101101000100001101011100010111)...(00101101000100001101011100010111)
#                   |------------ step --------------|
#                                                          ||   select good DNAs for next round
#                                                          \/
# New DNA(Depth 1): 00101101000100001101011100010111...00101101000100001101011100010111
#                                                          ||
#                                                          \/
# New DNA(Depth 2): ....
#
def process(depth=3):
    pass

def generate_new_dna_dir_name(dna_dir_name):
    dna_dir_name = dna_dir_name.rstrip('\\/')
    if '_round_' in dna_dir_name:
        raw_dna_dir_name, round = dna_dir_name.split('_round_')
        return raw_dna_dir_name + '_round_' + str(int(round)+1)
    else:
        return dna_dir_name + '_round_1'


help_msg = """
Usage:
    (a) find bypassed script sample
        >> python startup.py --file-type JS --file-path malicious_script --dna DNA_dir --start start_index --step DNA_size
        e.g.
        >> python startup.py --file-type JS --file-path samples/mal_script/0a0b692133dbba549c81dec49e1ba2ccf1b2bfea --dna DNA_JS/function_snippets --start 0 --step 32
      OR
    (b) find bypassed PE sample
        >> python3 startup.py --file-type PE --file-path malicious_pe --dna DNA_dir --start start_index --step DNA_size --tool housecallx_dir
        e.g.
        >> python3 startup.py --file-type PE --file-path samples/mal_pe/6d3e5e56984a7e91c7a8c434224b73886d413d1d1f435358f40bf78c71c1932d --dna DNA_PE/section_add --start 64 --step 32 --tool housecallx
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
    parser.add_option("--tool", dest="tool_path",
                      help="specify tool path", metavar="TOOL-PATH")

    (options, args) = parser.parse_args()
    # set config in logging
    basicConfig(filename='adversary_ml_{}.log'.format(os.getpid()), format='[%(asctime)s][%(levelname)s] - %(message)s', level=INFO)

    if options.file_type:
        if not os.path.exists(options.file_path):
            print('Cannot find {}'.format(options.file_path))
            exit(-1)
        if not os.path.exists(options.dna_path):
            print('Cannot find {}'.format(options.dna_path))
            exit(-1)
        info('Type: {}, Malicious File: {}, DNA: {}, Start Index: {}, Step: {}'.format(options.file_type, options.file_path, options.dna_path, options.start_index, options.step))
        if options.file_type == 'PE':
            process_one_group(TrendxAdversary.SCAN_TYPE_BINARY, options.file_path, options.dna_path, generate_new_dna_dir_name(options.dna_path), int(options.start_index), int(options.step), options.tool_path)
        elif options.file_type == 'JS':
            process_one_group(TrendxAdversary.SCAN_TYPE_SCRIPT, options.file_path, options.dna_path, generate_new_dna_dir_name(options.dna_path), int(options.start_index), int(options.step))
        else:
            print('Unsupported File Type')
    else:
        print(help_msg)
