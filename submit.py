import os, sys


def submit_file(file_path):
    print("> submit "+file_path)
    os.system('cuckoo submit --timeout 30 {}'.format(file_path))

def submit_dir(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            submit_file(os.path.join(root, name))

def submit(target_path):
    if os.path.isdir(target_path):
        submit_dir(target_path)
    elif os.path.isfile(target_path):
        submit_file(target_path)
    else:
        pass

if __name__ == '__main__':
    submit(sys.argv[1])

