import os
import sys
import time
from logging import *
from hcx_report import *
import re

def scan_by_housecallx(housecallx_path, sample_path):
    owd = os.getcwd()
    os.chdir(housecallx_path)
    print('Change Working Dir to: {}'.format(os.getcwd()))
    # remove previous log and trendx cache
    os.system('rm -f *.log trx_file_cache.dat')
    # scan by HouseCallX
    cmd  = 'wine HouseCallX.exe /RETRY /NOFB /REPORT "' + sample_path + '" 2> /dev/null'
    print('>> ' + cmd)
    begin = time.time()
    os.system(cmd)
    delta = time.time() - begin
    msg = 'Scan `{}` in TrendX, time delta: {}'.format(sample_path, delta)
    print(msg)
    info(msg)
    # find *_Report.log
    new_report_file = ''
    for filename in os.listdir('.'):
        pattern=re.compile(r"\d+_Report.log")
        m=pattern.match(filename)
        if m:
        #if '_Report.log' in filename:
            new_report_file = filename
            break

    if not os.path.exists(new_report_file):
        print('>> Cannot find HouseCallX report file, ' + new_report_file)
        exit(-1)

    scores = HouseCallXReport.get_scores(new_report_file)
    os.chdir(owd)
    print('Change Working Dir to: {}'.format(os.getcwd()))
    return scores

help_msg = """
Usage:
    python housecallx.py housecallx_path sample_dir
"""

if __name__ == '__main__':
    try:
        scan_by_housecallx(sys.argv[1], sys.argv[2])
    except Exception as e:
        print(e)
        print(help_msg)