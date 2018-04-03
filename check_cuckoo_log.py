import os, sys, json, shutil
import yara

class CuckooLogChecker:
    """"""
    def __init__(self):
        self.delete_mode = False
        self.threshold_score = 4.0
        self.total_count = 0
        self.count_lt = 0
        self.count_ge = 0
        self.baseline_info = {}
        self.matched_baseline = {}
        self.count_match = 0
        self.count_unmatch = 0
        self.matched_info = []
        self.baseline = []
        self.c_matches_base = 0
        self.c_matches_gen = 0

    def enable_delete_mode(self):
        self.delete_mode = True

    def show_statistics(self):
        print('******************************************')
        print('Total Count: {}'.format(self.total_count))
        print('Count of `less than`: {}'.format(self.count_lt))
        print('Count of `greater equal`: {}'.format(self.count_ge))
        print('******************************************')
        for key,value in self.baseline_info.items():
            print('{}:{}'.format(key,value))
        print('\n------------- behavior match result -------------\n')
        print('******************************************')
        print('Total Count: {}'.format(self.total_count))
        print('Count of `behavior unmatch`: {}'.format(self.count_unmatch))
        print('Count of `behavior match`: {}'.format(self.count_match))
        print('Count of `Baseline samples` in match: {}'.format(self.c_matches_base))
        print('Count of `new generated samples` in match: {}'.format(self.c_matches_gen))
        print('Total Baseline: {}'.format(len(self.baseline)))
        print('******************************************')
        for key,value in self.matched_baseline.items():
            print('{}:{}'.format(key,value))
        print('See matched_file_list.txt')

    def count_baseline_sample(self, target_path):
        dir_path, filename = os.path.split(target_path)
        baseline_name = filename.split('_')[0]
        if baseline_name in self.baseline_info.keys():
            self.baseline_info[baseline_name] += 1
        else:
            self.baseline_info[baseline_name] = 1

    def count_matched_sample(self, target_path):
        dir_path, filename = os.path.split(target_path)
        baseline_name = filename.split('_')[0]
        if baseline_name in self.matched_baseline.keys():
            self.matched_baseline[baseline_name] += 1
        else:
            self.matched_baseline[baseline_name] = 1

    def count_total_baseline(self, baseline_name):
        if baseline_name not in self.baseline:
            self.baseline.append(baseline_name)

    def extract_bhv(self, report_map, filename):
        descriptions = ''
        signatures = report_map['signatures']
        for sig in signatures:
            description = sig['description']
            descriptions += '%s\n' % description
        if not os.path.exists('signatures'):
            os.makedirs('signatures')
        with open(os.path.join('signatures', filename), 'w') as f:
            f.write(descriptions)

    def check_file(self, file_path):
        try:
            report_dir, report_filename = os.path.split(file_path)
            if 'report.json' != report_filename:
                return None
            task_dir, report_name = os.path.split(report_dir)
            task_path = os.path.join(task_dir, 'task.json')
            score = 0
            duration = 0
            target = ''
            isMatch = ''
            with open(file_path, 'r') as fh:
                reports = json.load(fh)
                score = reports['info']['score']
                duration = reports['info']['duration']
            with open(task_path, 'r') as fh_task:
                task = json.load(fh_task)
                target = task['target']
            filename = os.path.split(target)[1]
            baseline_name = filename.split('_')[0]
            rule_dir = 'baseline_rules/'
            rule_name = 'bhv_rule_%s' % (baseline_name)
            rule = yara.compile(rule_dir + rule_name)
            matches = rule.match(file_path)
            if matches:
                isMatch = 'BHVmatch'
                self.count_matched_sample(target)
                self.count_match += 1
                self.matched_info.append(filename)
                if 1 == len(filename.split('_')):
                    self.c_matches_base += 1
                else:
                    self.c_matches_gen += 1
            else:
                isMatch = 'BHVnotmatch'
                self.count_unmatch += 1
            with open(file_path, 'r') as f:
                reports = json.load(f)
                self.extract_bhv(reports, filename)
            if 1 == len(filename.split('_')):
                self.count_total_baseline(baseline_name)
            if score < self.threshold_score:
                if self.delete_mode:
                    if os.path.exists(target):
                        os.remove(target)
                    if os.path.exists(task_dir):
                        shutil.rmtree(task_dir)
                self.count_lt += 1
            else:
                self.count_ge += 1
                self.count_baseline_sample(target)
            self.total_count += 1
            return (score, duration, task_path, target, isMatch)
        except Exception as e:
            print(e)
            return None

    def check_dir(self, dir_path):
        result = []
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                if 'report.json' == name:
                    info = self.check_file(os.path.join(root, name))
                    if info:
                        result.append(info)
        return result

    def check(self, target_path):
        if os.path.isdir(target_path):
            return self.check_dir(target_path)
        elif os.path.isfile(target_path):
            return [self.check_file(target_path)]
        else:
            return []

help_msg = """
Usage:
    python check_cuckoo_log.py [-s|-d] target_path

    Options:
        -s : print summary information
        -d : delete all of failed samples
"""


if __name__ == '__main__':
    try:
        checker = CuckooLogChecker()
        if sys.argv[1] == '-s':
            info_list = checker.check(sys.argv[2])
            with open('bypassed_file_list.txt', 'w') as fh:
                for info in info_list:
                    # score, duration, task_path, target
                    # fh.write('{} {} {} {}\n'.format(info[0], info[1], info[2], info[3]))
                    fh.write('{} {} {}\n'.format(info[3], info[0], info[4]))
            with open('matched_file_list.txt', 'w') as ft:
                for file_path in checker.matched_info:
                    ft.write('{}\n'.format(file_path))
            checker.show_statistics()
        elif sys.argv[1] == '-d':
            checker.enable_delete_mode()
            checker.check(sys.argv[2])
        else:
            print(help_msg)
    except Exception as e:
        print(e)
        print(help_msg)
