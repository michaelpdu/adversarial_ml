import os, shutil
from tlsh_tool.tlsh_tool import *

class TLSHOutput:
    """"""

    def __init__(self, csv_file, data):
        self.data_ = {}
        # 
        with open(csv_file, 'r') as fh:
            hash_lines = fh.readlines()
        # 
        output_lines = data.split('\n')
        if output_lines[-1] == '':
            output_lines.remove('')

        for index in range(len(hash_lines)):
            file_info = hash_lines[index].split(',')[0]
            distance = output_lines[index].split('\t')[-1]
            self.data_[file_info] = int(distance)

class TLSHWrapper:
    """"""

    def __init__(self):
        pass

    def set_middle_dir(self, middle_dir):
        self.middle_dir = middle_dir
        if not os.path.exists(self.middle_dir):
            os.makedirs(self.middle_dir)

    def scan(self, target):
        csv_file = gen_csv(target, self.middle_dir)
        if None == csv_file:
            print('ERROR: failed to generate CSV file, {}'.format(target))
            return None
        else:
            csv_file = os.path.abspath(csv_file)
            previous_wd = os.getcwd()
            os.chdir(os.path.join(previous_wd, 'tools', 'tlsh_tool'))
            output_data = scan_csv(csv_file)
            os.chdir(previous_wd)
            tlsh_output = TLSHOutput(csv_file, output_data)
            # remove csv file
            os.remove(csv_file)
            return tlsh_output

    def scan_file(self, file_path):
        tlsh_ouput = self.scan(file_path)
        return int(tlsh_ouput.data_[file_path])

    def scan_dir(self, dir_path):
        tlsh_ouput = self.scan(dir_path)
        return tlsh_ouput.data_

if __name__ == '__main__':
    tlsh_wrapper = TLSHWrapper()
    tlsh_wrapper.set_middle_dir('UT/csv_dir/')
    tlsh_wrapper.scan_dir(r'/sa/github/adversary_ml/new_generated_samples/')
