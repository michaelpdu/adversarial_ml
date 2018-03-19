import os, sys, json

class CuckooLogChecker:
    """"""
    def __init__(self, timeout):
        self.timeout_ = timeout

    def check_file(self, file_path):
        with open(file_path, 'r') as fh:
            task = json.load(fh)
            target = task['target']
            if task['duration'] > self.timeout_:
                print('> Find executable file: {}'.format(target))
                return target
            else:
                return None

    def check_dir(self, dir_path):
        result = []
        for root, dirs, files in os.walk(dir_path):
            for name in files:
                if 'task.json' == name:
                    target = self.check_file(os.path.join(root, name))
                    if target:
                        result.append(target)
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
    file_list = checker.check(sys.argv[1])
    with open('bypassed_file_list.txt', 'w') as fh:
        for file_path in file_list:
            if file_path:
                print(file_path)
                fh.write('{}\n'.format(file_path))



