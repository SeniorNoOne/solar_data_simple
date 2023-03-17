import csv
import os.path
import os
import time
import numpy as np
import shutil
from datetime import datetime, timedelta


def timeit(func):
    def timed(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} took {end - start} seconds to execute")
        return result
    return timed


class FileProcessor:
    def __init__(self, filename, delimiter=","):
        self.file_dir = filename
        self.delimiter = delimiter

        if os.path.isfile(filename):
            with open(self.file_dir, "r", newline="") as input_file:
                self.has_header, self.col_num = self.get_file_info(input_file)

                if self.has_header:
                    self.file_reader = csv.DictReader(input_file, delimiter=delimiter)
                else:
                    self.file_reader = csv.DictReader(
                        input_file,
                        delimiter=delimiter,
                        fieldnames=[f"col{num}" for num in range(self.col_num)]
                    )
                self.header = list(self.file_reader.fieldnames)
                self.data = self.get_file_data()
                self.filtered_data = self.data
                self.filtered_header = self.header
        else:
            raise FileNotFoundError(f"Wrong file name or path - {filename}")


    def __iter__(self):
        return iter(self.data)

    def get_file_info(self, file):
        has_header = csv.Sniffer().has_header(file.read(1024))
        file.seek(0)

        col_num = len(file.readline().split(self.delimiter))
        file.seek(0)
        return has_header, col_num

    def get_file_data(self):
        result = {col: [] for col in self.header}
        for row in self.file_reader:
            for key, value in row.items():
                if not value:
                    value = result[key][-1]
                result[key].append(value)
        return result

    def write_col_in_file(self, col_name, filename, use_filtered=True):
        if col_name in self.filtered_data:
            data = self.filtered_data if use_filtered else self.data
            with open(filename, "w") as output_file:
                for val in data[col_name]:
                    output_file.write(str(val) + "\n")
        else:
            raise ValueError(f"There is no column with such name - {col_name}")

    def write_data_in_file(self, filename, sep=",", use_filtered=True):
        data = self.filtered_data if use_filtered else self.data
        with open(filename, "w") as output_file:
            for index, _ in enumerate(data[self.header[0]]):
                values_to_write = [str(data[col_name][index]) for col_name in data]
                output_file.write(sep.join(values_to_write) + "\n")

    def filter_by_date(self, data, col_name, filter_dates):
        filtered_data = {col_name: [] for col_name in self.header}
        if col_name in self.header:
            for index, date in enumerate(data[col_name]):
                if any([filter_date in date for filter_date in filter_dates]):
                    for col_name in self.header:
                        filtered_data[col_name].append(data[col_name][index])
        self.filtered_data = filtered_data

    def filter_by_value(self, data, col_name, min_val):
        filtered_data = {col_name: [] for col_name in self.header}
        if col_name in self.header:
            for index, value in enumerate(data[col_name]):
                value = float(value)
                if value > min_val:
                    for col_name in self.header:
                        filtered_data[col_name].append(data[col_name][index])
        self.filtered_data = filtered_data

    def drop_col_from_data(self, col_names_to_drop):
        for col_name in col_names_to_drop:
            if col_name in self.header:
                self.filtered_header.remove(col_name)
                self.filtered_data.pop(col_name)

    def shift_date(self, data, col_name, datetime_format, **kwargs):
        timeshift = timedelta(**kwargs)
        if col_name in self.header:
            for index, date in enumerate(data[col_name]):
                date = datetime.strptime(date, datetime_format)
                date = date + timeshift
                date = date.strftime(datetime_format)
                self.filtered_data[col_name][index] = date

    def preview(self):
        for col_name in self.filtered_data:
            print(f"{col_name} ({len(self.filtered_data[col_name])}) - "
                  f"{self.filtered_data[col_name][:10]}")
        print()

    def join_columns(self, data, columns_to_join, new_col_name, join_sep=" "):
        self.filtered_data[new_col_name] = []

        for index, val in enumerate(data[columns_to_join[0]]):
            for col_name in columns_to_join[1:]:
                val += join_sep + data[col_name][index]
                self.filtered_data[new_col_name].append(val)

        self.header.append(new_col_name)

    def split_columns(self, data, column_to_split, new_col_names, split_sep=" "):
        for col_name in new_col_names:
            self.filtered_data[col_name] = []

        if len(data[column_to_split][0].split(split_sep)) == len(new_col_names):
            for val in data[column_to_split]:
                val = val.split(split_sep)
                for col_name, new_val in zip(new_col_names, val):
                    self.filtered_data[col_name].append(new_val)
            self.header.extend(new_col_names)
        else:
            ValueError

    def calc_probability(self, data, col_name, time_col_name, interval=60):
        probability = []
        entropy = []
        data = data[col_name]

        for index in range(0, len(data) // interval):
            sum_ = sum(data[index * interval: (index + 1) * interval])
            for val in data[index * interval: (index + 1) * interval]:
                probability.append(val / sum_)
            entr = sum([-prob * np.emath.log(prob) for prob in probability[-interval::]])
            entropy.extend([entr] * 60)
        self.filtered_data["prob"] = probability
        self.filtered_data["entropy"] = entropy
        self.header.extend(["prob", "entropy"])
        # Лютый хардкод
        self.filtered_data[time_col_name] = self.filtered_data[time_col_name][:(index + 1) * interval]

    def to_float(self, data, col_name):
        for index, val in enumerate(data[col_name]):
            data[col_name][index] = float(val)
        self.filtered_data = data

    def subtract_datetime_data(self, td_real, values_real, format_1, td_ideal, values_ideal, format_2):
        td_real = [datetime.strptime(date, format_1) for date in td_real]
        td_ideal = [datetime.strptime(date, format_2) for date in td_ideal]

        td_diff = []
        values_diff = []

        for r_index, time in enumerate(td_real):
            if time in td_ideal:
                i_index = td_ideal.index(time)
                td_diff.append(time)
                values_diff.append(values_ideal[i_index] - values_real[r_index])
        self.filtered_data["entropy_diff"] = values_diff
        self.filtered_data["diff_time"] = [time.strftime("%H:%M") for time in td_diff]
        # hardcode
        self.header.extend(["entropy_diff", "diff_time"])


def test():
    file = FileProcessor("Photovoltaic array A measurements.csv")
    drop_cols = ['photovoltaic_measurement_reactive_power',
                 'photovoltaic_measurement_global_irradiance_pv_plane',
                 'photovoltaic_measurement_temperature_point_1',
                 'photovoltaic_measurement_temperature_point_2']
    file.drop_col_from_data(drop_cols)
    file.filter_by_date("2019-05-06", "photovoltaic_measurement_timestamp")
    print(file.filtered_data["photovoltaic_measurement_timestamp"][:10])
    file.shift_date("photovoltaic_measurement_timestamp", "%Y-%m-%d %H:%M:%S", hours=2)
    print(file.filtered_data["photovoltaic_measurement_timestamp"][:10])


def graph_1():
    # Graph 1
    # Real SP data
    FIRST_GRAPH_DIR = "graph_1/"
    os.makedirs(FIRST_GRAPH_DIR, exist_ok=True)
    file = FileProcessor("Photovoltaic array A measurements.csv")
    file.drop_col_from_data(drop_cols_file_1)
    file.filter_by_date(file.filtered_data, "photovoltaic_measurement_timestamp",
                        ["2019-04-29", "2019-04-30"])
    file.shift_date(file.filtered_data, "photovoltaic_measurement_timestamp",
                    "%Y-%m-%d %H:%M:%S", hours=2)
    file.filter_by_date(file.filtered_data, "photovoltaic_measurement_timestamp",
                        ["2019-04-29"])
    file.filter_by_value(file.filtered_data, "photovoltaic_measurement_active_power", 0)
    file.write_col_in_file("photovoltaic_measurement_timestamp",
                           FIRST_GRAPH_DIR + "time_vals_1.txt")
    file.write_col_in_file("photovoltaic_measurement_active_power",
                           FIRST_GRAPH_DIR + "power_vals_1.txt")
    file.write_data_in_file(FIRST_GRAPH_DIR + "graph_1.txt")


def graph_2():
    # Graph 2
    # Real SP data
    # NOTE THAT ALL DATA WERE OBTAINED MANUALLY
    SECOND_GRAPH_DIR = "graph_2/"
    os.makedirs(SECOND_GRAPH_DIR, exist_ok=True)


def graph_3():
    # Graph 3
    # Real load data
    THIRD_GRAPH_DIR = "graph_3/"
    os.makedirs(THIRD_GRAPH_DIR, exist_ok=True)
    file = FileProcessor("household_power_consumption.txt", delimiter=";")
    file.drop_col_from_data(drop_cols_file_2)
    file.join_columns(file.filtered_data, ["Date", "Time"], "Datetime")
    file.filter_by_date(file.filtered_data, "Datetime", ["24/11/2010", "23/11/2010"])
    file.shift_date(file.filtered_data, "Datetime", "%d/%m/%Y %H:%M:%S", hours=2)
    file.filter_by_date(file.filtered_data, "Datetime", ["24/11/2010"])
    file.write_col_in_file("Datetime", THIRD_GRAPH_DIR + "time_vals_3.txt")
    file.to_float(file.filtered_data, "Global_active_power")
    file.filtered_data["Global_active_power"] = [power * 1000 for power in file.filtered_data["Global_active_power"]]
    file.preview()
    file.write_col_in_file("Global_active_power", THIRD_GRAPH_DIR + "power_vals_3.txt")
    file.write_data_in_file(THIRD_GRAPH_DIR + "graph_3.txt")


def graph_4():
    # Graph 4
    # Ideal load data
    # NOTE THAT MATLAB USES DATA FROM GRAPH 3
    # SO IT'S MANDATORY TO MANUALLY COPY OUTPUT FILES FROM GRAPH 3 DIR
    THIRD_GRAPH_DIR = "graph_3/"
    FOURTH_GRAPH_DIR = "graph_4/"
    os.makedirs(FOURTH_GRAPH_DIR, exist_ok=True)
    copy_file(THIRD_GRAPH_DIR, FOURTH_GRAPH_DIR, file_extension="graph_3.txt")
    raw_graph_4 = FileProcessor(FOURTH_GRAPH_DIR + "graph_3.txt")
    raw_graph_4.split_columns(raw_graph_4.filtered_data, "col3", ["date", "time"])
    raw_graph_4.preview()
    raw_graph_4.to_float(raw_graph_4.filtered_data, "col2")
    length = len(raw_graph_4.filtered_data["col2"])
    mean_value = sum(raw_graph_4.filtered_data["col2"]) / length
    raw_graph_4.filtered_data["mean"] = [mean_value] * length
    raw_graph_4.preview()
    raw_graph_4.write_col_in_file("mean", FOURTH_GRAPH_DIR + "power_vals_4.txt")
    raw_graph_4.write_col_in_file("time", FOURTH_GRAPH_DIR + "time_vals_4.txt")


def graph_5():
    # Graph 5
    # Entropy
    # Uses files from Graph 1 and Graph 2
    FIRST_GRAPH_DIR = "graph_1/"
    SECOND_GRAPH_DIR = "graph_2/"
    FIFTH_GRAPH_DIR = "graph_5/"
    os.makedirs(FIFTH_GRAPH_DIR, exist_ok=True)
    copy_file(FIRST_GRAPH_DIR, FIFTH_GRAPH_DIR, file_extension="graph_1.txt")
    copy_file(SECOND_GRAPH_DIR, FIFTH_GRAPH_DIR, file_extension="graph_2.txt")

    r_file = FileProcessor(FIFTH_GRAPH_DIR + "graph_1.txt")
    r_file.filter_by_value(r_file.filtered_data, "col1", 0)
    r_file.split_columns(r_file.filtered_data, "col0", ["date", "time"])
    r_file.to_float(r_file.filtered_data, "col1")
    r_file.calc_probability(r_file.filtered_data, "col1", "time")
    r_file.preview()
    r_file.write_col_in_file("time", FIFTH_GRAPH_DIR + "inp_real_data_time_vals.txt")
    r_file.write_col_in_file("entropy", FIFTH_GRAPH_DIR + "inp_real_data_entropy.txt")
    r_file.write_col_in_file("prob", FIFTH_GRAPH_DIR + "inp_real_data_prob.txt")

    i_file = FileProcessor(FIFTH_GRAPH_DIR + "graph_2.txt")
    i_file.to_float(i_file.filtered_data, "col1")
    i_file.calc_probability(i_file.filtered_data, "col1", "col0")
    i_file.preview()
    i_file.write_col_in_file("col0", FIFTH_GRAPH_DIR + "inp_ideal_data_time_vals.txt")
    i_file.write_col_in_file("entropy", FIFTH_GRAPH_DIR + "inp_ideal_data_entropy.txt")
    i_file.write_col_in_file("prob", FIFTH_GRAPH_DIR + "inp_ideal_data_prob.txt")

    i_file.subtract_datetime_data(
        r_file.filtered_data["time"],
        r_file.filtered_data["entropy"],
        "%H:%M:%S",
        i_file.filtered_data["col0"],
        i_file.filtered_data["entropy"],
        "%H:%M"
    )
    i_file.preview()

    i_file.write_col_in_file("entropy_diff", FIFTH_GRAPH_DIR + "inp_diff_entropy.txt")
    i_file.write_col_in_file("diff_time", FIFTH_GRAPH_DIR + "inp_diff_data_time_vals.txt")


def graph_6():
    # Graph 6
    # Entropy
    THIRD_GRAPH_DIR = "graph_3/"
    FOURTH_GRAPH_DIR = "graph_4/"
    SIXTH_GRAPH_DIR = "graph_6/"
    os.makedirs(SIXTH_GRAPH_DIR, exist_ok=True)
    copy_file(THIRD_GRAPH_DIR, SIXTH_GRAPH_DIR, file_extension="graph_3.txt")
    copy_file(FOURTH_GRAPH_DIR, SIXTH_GRAPH_DIR, file_extension="time_vals_4.txt")
    copy_file(FOURTH_GRAPH_DIR, SIXTH_GRAPH_DIR, file_extension="power_vals_4.txt")

    r_file = FileProcessor(SIXTH_GRAPH_DIR + "graph_3.txt")
    r_file.filter_by_value(r_file.filtered_data, "col2", 0)
    r_file.to_float(r_file.filtered_data, "col2")
    r_file.split_columns(r_file.filtered_data, "col3", ["date", "time"])
    r_file.calc_probability(r_file.filtered_data, "col2", "time")
    r_file.preview()
    r_file.write_col_in_file("time", SIXTH_GRAPH_DIR + "out_real_data_time_vals.txt")
    r_file.write_col_in_file("entropy", SIXTH_GRAPH_DIR + "out_real_data_entropy.txt")
    r_file.write_col_in_file("prob", SIXTH_GRAPH_DIR + "out_real_data_prob.txt")

    i_file_time = FileProcessor(SIXTH_GRAPH_DIR + "time_vals_4.txt")
    i_file_power = FileProcessor(SIXTH_GRAPH_DIR + "power_vals_4.txt")
    i_file = merge_two_to_one(i_file_time, i_file_power)

    i_file.to_float(i_file.filtered_data, "col0_merge")
    i_file.calc_probability(i_file.filtered_data, "col0_merge", "col0")
    i_file.preview()

    i_file.write_col_in_file("col0", SIXTH_GRAPH_DIR + "out_ideal_data_time_vals.txt")
    i_file.write_col_in_file("entropy", SIXTH_GRAPH_DIR + "out_ideal_data_entropy.txt")
    i_file.write_col_in_file("prob", SIXTH_GRAPH_DIR + "out_ideal_data_prob.txt")

    i_file.subtract_datetime_data(
        r_file.filtered_data["time"],
        r_file.filtered_data["entropy"],
        "%H:%M:%S",
        i_file.filtered_data["col0"],
        i_file.filtered_data["entropy"],
        "%H:%M:%S",
    )
    i_file.preview()

    i_file.write_col_in_file("entropy_diff", SIXTH_GRAPH_DIR + "out_diff_entropy.txt")
    i_file.write_col_in_file("diff_time", SIXTH_GRAPH_DIR + "out_diff_data_time_vals.txt")


def graph_7():
    # Graph 7
    # Entropy and relay graph
    FIFTH_GRAPH_DIR = "graph_5/"
    SIXTH_GRAPH_DIR = "graph_6/"
    SEVENTH_GRAPH_DIR = "graph_7/"
    os.makedirs(SEVENTH_GRAPH_DIR, exist_ok=True)
    copy_file(FIFTH_GRAPH_DIR, SEVENTH_GRAPH_DIR, file_extension="inp_diff_data_time_vals.txt")
    copy_file(FIFTH_GRAPH_DIR, SEVENTH_GRAPH_DIR, file_extension="inp_diff_entropy.txt")
    copy_file(SIXTH_GRAPH_DIR, SEVENTH_GRAPH_DIR, file_extension="out_diff_data_time_vals.txt")
    copy_file(SIXTH_GRAPH_DIR, SEVENTH_GRAPH_DIR, file_extension="out_diff_entropy.txt")

    inp_file_time = FileProcessor(SEVENTH_GRAPH_DIR + "inp_diff_data_time_vals.txt")
    inp_file_diff = FileProcessor(SEVENTH_GRAPH_DIR + "inp_diff_entropy.txt")
    i_file = merge_two_to_one(inp_file_time, inp_file_diff)
    i_file.to_float(i_file.filtered_data, "col0_merge")
    i_file.preview()

    out_file_time = FileProcessor(SEVENTH_GRAPH_DIR + "out_diff_data_time_vals.txt")
    out_file_diff = FileProcessor(SEVENTH_GRAPH_DIR + "out_diff_entropy.txt")
    o_file = merge_two_to_one(out_file_time, out_file_diff)
    o_file.to_float(o_file.filtered_data, "col0_merge")
    o_file.preview()

    i_file.subtract_datetime_data(
        i_file.filtered_data["col0"],
        i_file.filtered_data["col0_merge"],
        "%H:%M",
        o_file.filtered_data["col0"],
        o_file.filtered_data["col0_merge"],
        "%H:%M",
    )
    i_file.preview()
    data = signum(i_file.filtered_data["entropy_diff"], 1, 0.5)
    i_file.filtered_data["step"] = data
    i_file.preview()
    i_file.write_col_in_file("entropy_diff", SEVENTH_GRAPH_DIR + "total_entropy_diff.txt")
    i_file.write_col_in_file("diff_time", SEVENTH_GRAPH_DIR + "total_entropy_time.txt")
    i_file.write_col_in_file("step", SEVENTH_GRAPH_DIR + "total_step.txt")


def merge_two_to_one(file_1, file_2):
    file_2_data = {f"{col_name}_merge": file_2.filtered_data[col_name] for
                   col_name in file_2.filtered_data}
    for col_name in file_2_data:
        file_1.filtered_data[col_name] = file_2_data[col_name]
    return file_1


def signum(data, offset=0, factor=1):
    result = []
    for val in data:
        if val > 0:
            result.append(factor * (offset + 1))
        elif val < 0:
            result.append(factor * (offset - 1))
        else:
            result.append(factor * offset)
    return result


def copy_file(source, target, file_extension=".txt"):
    for file_name in os.listdir(source):
        if file_name.endswith(file_extension):
            src_file_path = os.path.join(source, file_name)
            dst_file_path = os.path.join(target, file_name)
            shutil.copy(src_file_path, dst_file_path)


if __name__ == "__main__":
    drop_cols_file_1 = ['photovoltaic_measurement_reactive_power',
                        'photovoltaic_measurement_global_irradiance_pv_plane',
                        'photovoltaic_measurement_temperature_point_1',
                        'photovoltaic_measurement_temperature_point_2']

    drop_cols_file_2 = ["Global_reactive_power",
                        "Voltage",
                        "Global_intensity",
                        "Sub_metering_1",
                        "Sub_metering_2",
                        "Sub_metering_3"]

    graph_1()
    graph_2()
    graph_3()
    graph_4()
    graph_5()
    graph_6()
    graph_7()
