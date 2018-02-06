import os
import sys
from housecallx_report import *

def scan_by_housecallx(housecallx_path, path):
    owd = os.getcwd()
    os.chdir(housecallx_path)
    print('Change Working Dir to: {}'.format(os.getcwd()))
    # remove previous log and trendx cache
    os.system('rm -f *.log trx_file_cache.dat')
    # scan by HouseCallX
    cmd  = 'wine HouseCallX.exe /RETRY /NOFB /REPORT ' + path
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
    report = HouseCallXReport(new_report_file)

    os.chdir(owd)
    print('Change Working Dir to: {}'.format(os.getcwd()))
    return report.get_scores()



