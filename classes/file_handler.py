import csv
import os
from datetime import datetime, timedelta


class FileHandler:
    def __init__(self, filename, delimiter=",", emtpy_vals=(" ", "?"), dt_format=None):
        self.filename = filename
        self.delimiter = delimiter
        self.empty_vals = emtpy_vals
        self.dt_format = dt_format

        if os.path.isfile(filename):
            with open(self.filename, "r", newline="") as self.input_file:
                self._has_header, self.col_num = self._get_file_info()

                if self._has_header:
                    self.file_reader = csv.DictReader(self.input_file, delimiter=delimiter)
                else:
                    self.file_reader = csv.DictReader(
                        self.input_file,
                        delimiter=delimiter,
                        fieldnames=[f"col{num}" for num in range(self.col_num)]
                    )
                self.header = list(self.file_reader.fieldnames)
                self.raw_data, self.data = self._get_file_data()
                self.numeric_cols = self._get_numeric_col()
        else:
            raise FileNotFoundError(f"Wrong file name or path - {filename}")

    @staticmethod
    def _get_col_len(data):
        col_len = [len(col) for col in data.values()]
        if len(set(col_len)) == 1:
            return col_len[-1]
        else:
            raise ValueError("Columns should have same length")

    def _get_file_info(self):
        has_header = csv.Sniffer().has_header(self.input_file.read(1024))
        self.input_file.seek(0)
        col_num = len(self.input_file.readline().split(self.delimiter))
        self.input_file.seek(0)
        return has_header, col_num

    def _get_file_data(self):
        raw_data = {col: [] for col in self.header}
        data = {col: [] for col in self.header}
        for row in self.file_reader:
            for key, val in row.items():
                if not val or val in self.empty_vals:
                    # if there is record with empty value previous non-empty value will be used
                    val = raw_data[key][-1]
                raw_data[key].append(val)
                data[key].append(val)
        return raw_data, data

    def _get_numeric_col(self, sample_size=5):
        is_col_numeric = dict()
        for col_name in self.header:
            sample = (val.isnumeric() or val.replace(".", "").replace("-", "").isnumeric() for
                      val in self.raw_data[col_name][:sample_size])
            is_col_numeric[col_name] = all(sample)
        return is_col_numeric

    def convert_data(self, use_raw=False):
        data = self.raw_data if use_raw else self.data
        for col_name in self.data:
            if self.numeric_cols.get(col_name):
                data[col_name] = [float(val) for val in data[col_name]]

    def filter_by_date(self, col_name, filter_dates, use_raw=False):
        data = self.raw_data if use_raw else self.data
        f_data = {col_name: [] for col_name in data}
        if col_name in data:
            for index, date in enumerate(data[col_name]):
                if any([filter_date in date for filter_date in filter_dates]):
                    for col_name in data:
                        f_data[col_name].append(data[col_name][index])
            self.data = f_data
        else:
            ValueError(f"There is no column with such name - {col_name}")

    def filter_by_value(self, col_name, min_val=None, max_val=None, use_raw=False):
        data = self.raw_data if use_raw else self.data
        if col_name in data:
            f_indexes = None
            if min_val is not None and max_val is not None:
                f_indexes = [index for index, val in enumerate(data[col_name]) if
                             min_val <= val <= max_val]
            elif min_val is not None:
                f_indexes = [index for index, val in enumerate(data[col_name]) if min_val <= val]
            elif max_val is not None:
                f_indexes = [index for index, val in enumerate(data[col_name]) if val <= max_val]
            self.filter_by_index(f_indexes, use_raw)

    def filter_by_index(self, indexes, use_raw=False):
        data = self.raw_data if use_raw else self.data
        f_data = {col_name: [] for col_name in data}
        for index in indexes:
            for col_name in data:
                f_data[col_name].append(data[col_name][index])
        self.data = f_data

    def write_col_in_file(self, col_name, filename, use_raw=False, write_header=False):
        data = self.raw_data if use_raw else self.data
        if col_name in data:
            with open(filename, "w") as output_file:
                if write_header:
                    output_file.write(col_name + "\n")
                for val in data[col_name]:
                    output_file.write(str(val) + "\n")
        else:
            raise ValueError(f"There is no column with such name - {col_name}")

    def write_data_in_file(self, filename, delimiter=",", use_raw=False, write_header=False):
        data = self.raw_data if use_raw else self.data
        with open(filename, "w") as output_file:
            if write_header:
                output_file.write(delimiter.join([col_name for col_name in data]))
            for index in range(self._get_col_len(data)):
                values_to_write = [str(data[col_name][index]) for col_name in data]
                output_file.write(delimiter.join(values_to_write) + "\n")

    def drop_col_from_data(self, col_names_to_drop, use_raw=False):
        data = self.raw_data if use_raw else self.data
        for col_name in col_names_to_drop:
            if col_name in data:
                data.pop(col_name)
            else:
                raise ValueError(f"There is no column with name '{col_name}' if data")

    def shift_date(self, col_name, use_raw=False, **kwargs):
        data = self.raw_data if use_raw else self.data
        timeshift = timedelta(**kwargs)
        if col_name in data:
            for index, date in enumerate(data[col_name]):
                date = datetime.strptime(date, self.dt_format) + timeshift
                date = date.strftime(self.dt_format)
                data[col_name][index] = date
        else:
            raise ValueError(f"There is no column with name '{col_name}' if data")

    def preview(self, size=10, use_raw=False):
        data = self.raw_data if use_raw else self.data
        for col_name in data:
            print(f"{col_name} ({len(data[col_name])}) - {data[col_name][:size]}")
        print()

    def join_columns(self, columns_to_join, new_col_name, delimiter=",", use_raw=False):
        data = self.raw_data if use_raw else self.data
        col_len = self._get_col_len(data)
        self.data[new_col_name] = []
        for index in range(col_len):
            val = [data[col_name][index] for col_name in columns_to_join]
            self.data[new_col_name].append(delimiter.join(val))

    def split_columns(self, column_to_split, new_col_names, delimiter=",", use_raw=False):
        data = self.raw_data if use_raw else self.data
        for col_name in new_col_names:
            self.data[col_name] = []
        if len(data[column_to_split][0].split(delimiter)) == len(new_col_names):
            for val in data[column_to_split]:
                for col_name, new_val in zip(new_col_names, val.split(delimiter)):
                    self.data[col_name].append(new_val)
        else:
            raise ValueError("Number of sub columns and new_col_names do not match")

    def merge_two_to_one(self, other, use_raw=False):
        other_data = other.raw_data if use_raw else other.data
        data = self.raw_data if use_raw else self.data
        for col_name, val in other_data.items():
            new_col_name = f"{col_name}_merged"
            data[new_col_name] = other_data[col_name]
            self.numeric_cols[new_col_name] = other.numeric_cols[col_name]

    def subtract_col(self, dt_col_name, data_col_name, other, other_dt_col_name,
                     other_data_col_name, use_raw=False, dt_diff_col_name=None,
                     data_diff_col_name=None):
        data = self.raw_data if use_raw else self.data
        other_data = other.raw_data if use_raw else other.data

        dt = [datetime.strptime(date, self.dt_format) for date in data[dt_col_name]]
        other_dt = [datetime.strptime(date, other.dt_format) for date in
                    other_data[other_dt_col_name]]

        dt_diff = []
        val_diff = []

        for index, dt_val in enumerate(dt):
            if dt_val in other_dt:
                other_index = other_dt.index(dt_val)
                dt_diff.append(dt_val.strftime(self.dt_format))
                val_diff.append(data[data_col_name][index] -
                                other_data[other_data_col_name][other_index])

        dt_diff_col_name = dt_diff_col_name if dt_diff_col_name else "diff_time"
        data_diff_col_name = data_diff_col_name if data_diff_col_name else "diff_data"
        data[dt_diff_col_name] = dt_diff
        data[data_diff_col_name] = val_diff
