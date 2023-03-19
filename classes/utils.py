import os
import shutil
import time


def copy_files(source, target, file_extension=".txt"):
    for file_name in os.listdir(source):
        if file_name.endswith(file_extension):
            src_file_path = os.path.join(source, file_name)
            dst_file_path = os.path.join(target, file_name)
            shutil.copy(src_file_path, dst_file_path)


def timeit(func):
    def timed(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} took {end - start} seconds to execute")
        return result
    return timed


def make_dir(dir_name):
    os.makedirs(dir_name, exist_ok=True)
