import os, sys, json

class CuckooLogChecker:
    """"""
    def __init__(self, timeout):
        self.timeout_ = timeout

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

if __name__ == '__main__':
    checker = CuckooLogChecker(60)
    info_list = checker.check(sys.argv[1])
    with open('bypassed_file_list.txt', 'w') as fh:
        for info in info_list:
            fh.write('{} {} {} {}\n'.format(info[0], info[1], info[2], info[3]))



