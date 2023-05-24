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


def truncate_data(data, lower_bound=None, upper_bound=None):
    truncated_data = []
    if lower_bound:
        for val in data:
            if val >= lower_bound:
                truncated_data.append(val)
            else:
                truncated_data.append(lower_bound)
    data = truncated_data
    truncated_data = []
    if upper_bound:
        for val in data:
            if val <= upper_bound:
                truncated_data.append(val)
            else:
                truncated_data.append(lower_bound)
    return truncated_data


def input_calc(voltage, tr_factor):
    DIR = 'graph_1\\'

    with open(DIR + 'res_data_vals_1.txt', 'w') as res_f:
        power_f = open(DIR + 'power_data_vals_1.txt')
        power_data = [float(data) for data in power_f.readlines()]

        l_bound = tr_factor * max(power_data)
        u_bound = (1 - tr_factor) * max(power_data)

        power_data_tr = truncate_data(power_data, l_bound, u_bound)
        with open(DIR + 'power_data_vals_tr_1.txt', 'w') as p_f:
            for power_val in power_data_tr:
                p_f.write(str(power_val) + '\n')

        power_data = [voltage * voltage / 4 / data for data in power_data_tr]
        for data in power_data:
            res_f.write(str(2 * data) + '\n')
        res_f.close()


def output_calc(voltage, tr_factor):
    DIR = 'graph_3\\'
    voltage /= 2

    with open(DIR + 'res_data_vals_3.txt', 'w') as res_f:
        power_f = open(DIR + 'data_vals_3.txt')
        power_data = [float(data) for data in power_f.readlines()]

        l_bound = tr_factor * max(power_data)
        u_bound = (1 - tr_factor) * max(power_data)

        power_data_tr = truncate_data(power_data, l_bound, u_bound)
        with open(DIR + 'power_data_vals_tr_3.txt', 'w') as p_f:
            for power_val in power_data_tr:
                p_f.write(str(power_val) + '\n')

        power_data = [voltage * voltage / data for data in power_data_tr]
        for data in power_data:
            res_f.write(str(data) + '\n')
        res_f.close()
