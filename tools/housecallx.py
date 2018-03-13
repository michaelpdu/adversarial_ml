import os
import sys
from hcx_report import *

def scan_by_housecallx(housecallx_path, sample_path):
    owd = os.getcwd()
    os.chdir(housecallx_path)
    print('Change Working Dir to: {}'.format(os.getcwd()))
    # remove previous log and trendx cache
    os.system('rm -f *.log trx_file_cache.dat')
    # scan by HouseCallX
    cmd  = 'wine HouseCallX.exe /RETRY /NOFB /REPORT "' + sample_path + '"'
    print('>> ' + cmd)
    os.system(cmd)
    # find *_Report.log
    new_report_file = ''
    for filename in os.listdir('.'):
        if '_Report.log' in filename:
            new_report_file = filename
            break
    if not os.path.exists(new_report_file):
        print('>> Cannot find HouseCallX report file, ' + new_report_file)
        exit(-1)

    scores = HouseCallXReport.get_scores(new_report_file)
    os.chdir(owd)
    print('Change Working Dir to: {}'.format(os.getcwd()))
    return scores



