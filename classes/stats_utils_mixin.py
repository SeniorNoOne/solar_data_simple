from math import log


class StatsUtilsMixin:
    def __init__(self):
        self.raw_data = dict()
        self.data = dict()

    def calc_probability(self, col_name, time_col_name, interval=60, use_raw=False):
        probability = []
        entropy = []
        data = self.raw_data if use_raw else self.data

        if col_name in data:
            for index in range(0, len(data[col_name]) // interval):
                interval_sum = sum(data[col_name][index * interval: (index + 1) * interval])
                for val in data[col_name][index * interval: (index + 1) * interval]:
                    probability.append(val / interval_sum)
                entropy_val = sum([-prob * log(prob) for prob in probability[-interval::]])
                entropy.extend([entropy_val] * 60)

            data["probability"] = probability
            data["entropy"] = entropy
            data["stats_time"] = data[time_col_name][:(index + 1) * interval]
        else:
            raise ValueError(f"There is no such col if data - {col_name}")

    def signum(self, col_name, offset=0, factor=1, use_raw=False):
        data = self.raw_data if use_raw else self.data
        result = []
        for val in data[col_name]:
            if val > 0:
                result.append(factor * (offset + 1))
            elif val < 0:
                result.append(factor * (offset - 1))
            else:
                result.append(factor * offset)
        data[f"{col_name}_signum"] = result
