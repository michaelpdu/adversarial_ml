import os, sys, json, shutil

class CuckooLogChecker:
    """"""
    def __init__(self):
        self.delete_mode = False
        self.threshold_score = 4.0
        self.total_count = 0
        self.count_lt = 0
        self.count_ge = 0

    def enable_delete_mode(self):
        self.delete_mode = True

    def show_statistics(self):
        print('******************************************')
        print('Total Count: {}'.format(self.total_count))
        print('Count of `less than`: {}'.format(self.count_lt))
        print('Count of `great equal`: {}'.format(self.count_ge))
        print('******************************************')

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
            with open(file_path, 'r') as fh:
                reports = json.load(fh)
                score = reports['info']['score']
                duration = reports['info']['duration']
            with open(task_path, 'r') as fh_task:
                task = json.load(fh_task)
                target = task['target']
            if score < self.threshold_score:
                if self.delete_mode:
                    if os.path.exists(target):
                        os.remove(target)
                    if os.path.exists(task_dir):
                        shutil.rmtree(task_dir)
                self.count_lt += 1
            else:
                self.count_ge += 1
            self.total_count += 1
            return (score, duration, task_path, target)
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
                    fh.write('{} {} {} {}\n'.format(info[0], info[1], info[2], info[3]))
            checker.show_statistics()
        elif sys.argv[1] == '-d':
            checker.enable_delete_mode()
            checker.check(sys.argv[2])
        else:
            print(help_msg)
    except Exception as e:
        print(e)
        print(help_msg)
