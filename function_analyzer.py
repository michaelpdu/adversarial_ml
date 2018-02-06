import os
import sys

FUNCTION_ANALYZER = r'ssa_function_extraction.js'

def process(target_path, dest_dir):
    if os.path.isfile(target_path):
        process_file(target_path, dest_dir)
    elif os.path.isdir(target_path):
        process_dir(target_path, dest_dir)

def process_dir(target_path, dest_dir):
    data = []
    for root, dirs, files in os.walk(target_path):
        print root
        for name in files:
            l = process_file(os.path.join(root, name), dest_dir)
            if l is not None:
                data.append(l)
    return data

def process_file(filename, dest_dir):
    cmd = r'node %s "%s" "%s"' % (FUNCTION_ANALYZER, filename, dest_dir)
    os.system(cmd)

help_msg = """
    Usage:
        python function_analyzer.py target dest_dir
"""

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print help_msg
        exit(0)
    if not os.path.exists(sys.argv[1]):
        print 'target file not exists'
        exit(0)
    process(sys.argv[1], sys.argv[2])