import os
import sys
import json
import hashlib
import lief
import array


class PESectionExtractor(object):
    def __init__(self):
        pass
    
    def set_dest_folder(self, dest_folder):
        self.dest_folder_ = dest_folder
        if not os.path.exists(self.dest_folder_):
            os.makedirs(self.dest_folder_)

    def extract_file(self, file_path):
        with open(file_path, 'rb') as fh:
            bytez = bytes(fh.read())
            bytez = array.array('B', bytez).tolist()
            binary = lief.PE.parse(bytez)
            for section in binary.sections:
                # print(section.content)
                print('Name: {}, Content Length: {}'.format(section.name, len(section.content)))
                if len(section.content) > 0:
                    md5_hash = hashlib.md5()
                    content = ''.join(str(e) for e in section.content)
                    md5_hash.update(content.encode('utf-8'))
                    md5_string = md5_hash.hexdigest()
                    with open(os.path.join(self.dest_folder_, md5_string), 'w') as fh_section:
                        fh_section.write('section_add\n')
                        for item in section.content:
                            fh_section.write('{} '.format(item))
                        # fh_section.write(section.content)

    def extract(self, target_path):
        if os.path.isdir(target_path):
            for root, dirs, files in os.walk(target_path):
                for name in files:
                    self.extract_file(os.path.join(root, name))
        elif os.path.isfile(target_path):
            self.extract_file(target_path)
        else:
            print('ERROR: {} is NOT directory or file'.format(target_path))

help_msg = """
Usage:
    python tool.py PE_target_path dest_path
"""

if __name__ == "__main__":
    section_extractor = PESectionExtractor()
    section_extractor.set_dest_folder(sys.argv[2])
    section_extractor.extract(sys.argv[1])