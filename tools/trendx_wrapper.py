import os
from ml_tool_interface import *
from trendx_tool.run import *
from housecallx import *

class TrendXWrapper(MLToolInterface):
    """"""

    def __init__(self, config):
        self.config_ = config
        self.hcx_path_ = ''

    def set_hcx(self, hcx_path):
        self.hcx_path_ = hcx_path

    def scan_pe_file(self, sample_path):
        """
        Return Value
            (decision, probability)
        """
        raise NotImplementedError("TrendXWrapper.scan_pe_file does not implemented!")

    def scan_pe_dir(self, sample_dir):
        """
        Return Value
            {
                file_path: (decision, probability),
                file_path: (decision, probability),
                ...
            }
        """
        return_scores = {}
        scores = scan_by_housecallx(self.hcx_path_, sample_dir)
        for key, value in scores.items():
            return_scores[os.path.join(sample_dir, key)] = value
        return return_scores

    def scan_pe_list(self, sample_list):
        """
        Return Value
            {
                file_path: (decision, probability),
                file_path: (decision, probability),
                ...
            }
        """
        raise NotImplementedError("TrendXWrapper.scan_pe_list does not implemented!")

    def scan_script_file(self, sample_path):
        """
        Return Value
            (decision, probability)
        """
        m = JSModel()
        prob = m.predictfile(sample_path)
        decision = 0
        if prob < 0.5:
            decision = 1
        return (decision, 1-prob)
    
    def scan_script_dir(self, sample_dir):
        """
        Return Value
            {
                file_path: (decision, probability),
                file_path: (decision, probability),
                ...
            }
        """
        result = {}
        for root, dirs, files in os.walk(sample_dir):
            for name in files:
                file_path = os.path.abspath(os.path.join(root, name))
                result[file_path] = self.scan_script_file(file_path)
        return result

    def scan_script_list(self, sample_list):
        """
        Return Value
            {
                file_path: (decision, probability),
                file_path: (decision, probability),
                ...
            }
        """
        result = {}
        for sample_path in sample_list:
            sample_path = os.path.abspath(sample_path)
            result[sample_path] = self.scan_script_file(sample_path)
        return result