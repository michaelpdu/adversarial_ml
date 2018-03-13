
from logging import *


class AdversaryTrendX:
    """"""

    def __init__(self, config):
        self.config_ = config
        self.scan_type_ = self.config_['trendx']['scan_type']
        self.dest_dir_ = self.config_['common']['generated_dir']

    def set_malicious_file(self, file_path):
        info('Set malicious file path: {}'.format(file_path))
        self.mal_file_path = file_path
        dir_path, file_name = os.path.split(file_path)
        name_wo_ext, ext = os.path.splitext(file_name)
        self.mal_file_name_wo_ext = name_wo_ext

    

