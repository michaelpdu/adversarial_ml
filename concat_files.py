import os
import sys
from hashlib import md5

FUNCTION_ANALYZER = r'ssa_function_extraction.js'

def process(ori_file, fun_code_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(ori_file, 'r') as fh:
        content = fh.read()
    for root, dirs, files in os.walk(fun_code_dir):
        for name in files:
            with open(os.path.join(root, name), 'r') as fh:
                fun_code_content = fh.read()
            concat_content = content +'\n\n\n//function code\n' + fun_code_content
            # use md5 value as file name
            hash_md5 = md5()
            hash_md5.update(concat_content)
            filename = hash_md5.hexdigest()
            with open(os.path.join(output_dir,filename), 'w') as fh:
                fh.write(concat_content)

help_msg = """
    Usage:
        python concat_files.py ori_file fun_code_dir output_dir
"""

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print help_msg
        exit(0)
    if not os.path.exists(sys.argv[1]):
        print 'Cannot find: {}'.format(sys.argv[1])
        exit(0)
    if not os.path.exists(sys.argv[2]):
        print 'Cannot find: {}'.format(sys.argv[2])
        exit(0)
    process(sys.argv[1], sys.argv[2], sys.argv[3])