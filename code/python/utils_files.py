import os, errno, shutil
from pathlib import Path


def remove_file_dir(path, is_dir = False):
    try:
        if(is_dir):
            shutil.rmtree(path=path)
        else:
            os.remove(path=path)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred

def make_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def clear_dir(path):
    remove_file_dir(path, is_dir=True)
    make_dir(path)

def read_file_into_array(file_name):
    with open(file_name) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content


def check_if_exists(path):
    file_or_dir = Path(path)
    if file_or_dir.exists():
        return True
    return False


def add_row_to_csv(path, headers, values):
    if not os.path.exists(path):
        file = open(path, 'w+')
        file.write(','.join(map(str, headers)) + '\n')
    else:
        file = open(path, 'a')
    file.write(','.join(map(str, values)) + '\n')
