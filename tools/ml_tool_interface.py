
class MLToolInterface(object):
    """"""

    def scan_pe_file(self, sample_path):
        """
        Return Value
            (decision, probability)
        """
        raise NotImplementedError("MLToolInterface.scan_pe_file does not implemented!")

    def scan_pe_dir(self, sample_dir):
        """
        Return Value
            {
                file_path: (decision, probability),
                file_path: (decision, probability),
                ...
            }
        """
        raise NotImplementedError("MLToolInterface.scan_pe_dir does not implemented!")

    def scan_pe_list(self, sample_list):
        """
        Return Value
            {
                file_path: (decision, probability),
                file_path: (decision, probability),
                ...
            }
        """
        raise NotImplementedError("MLToolInterface.scan_pe_list does not implemented!")

    def scan_script_file(self, sample_path):
        """
        Return Value
            (decision, probability)
        """
        raise NotImplementedError("MLToolInterface.scan_script_file does not implemented!")
    
    def scan_script_dir(self, sample_dir):
        """
        Return Value
            {
                file_path: (decision, probability),
                file_path: (decision, probability),
                ...
            }
        """
        raise NotImplementedError("MLToolInterface.scan_script_dir does not implemented!")

    def scan_script_list(self, sample_list):
        """
        Return Value
            {
                file_path: (decision, probability),
                file_path: (decision, probability),
                ...
            }
        """
        raise NotImplementedError("MLToolInterface.scan_script_list does not implemented!")