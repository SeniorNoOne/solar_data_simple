# import numpy as np

# graph 2
def process_time_file():
    formatted_time_file = open("formatted_time_file.txt", "w")

    with open("time.txt", "r") as time_file:
        for line in time_file:
            line = line.replace("\n", "")
            line = f'"{line}"\n'
            formatted_time_file.write(line)


def process_power_file():
    formatted_power_file = open("formatted_power_file.txt", "w")

    with open("power.txt", "r") as power_file:
        for line in power_file:
            line = line.replace("\n", "")
            line = line.replace(",", ".")
            line = f"{line}\n"
            formatted_power_file.write(line)


# graph 3
def process_household_data():
    formatted_household_data = open("formatted_household_data.txt", "w")

    with open("household_power_consumption.txt") as household_data:
        next(household_data)
        header = "Date;Time;Active_consumed_energy;Is_full\n"
        formatted_household_data.write(header)
        for line in household_data:
            line = to_float(line.split(";"))
            date, time, g_ap, g_rp, v, g_intens, sub_m1, sub_m2, sub_m3 = line
            ae_consumed = g_ap * 1000 / 60
            result_str = f"{date};{time};{ae_consumed},\n"
            formatted_household_data.write(result_str)


def get_household_data_by_date(filter_date):
    with open("formatted_household_data.txt") as household_data:
        next(household_data)
        house_hold_time = open("formatted_household_datetime.txt", "w")
        house_hold_energy = open("formatted_household_energy.txt", "w")
        for line in household_data:
            date, time, energy = line.split(";")
            if date == filter_date:
                time = f'"{time}"\n'
                house_hold_time.write(time)
                house_hold_energy.write(energy)


# SP p-v curves
def process_pv_array_data():
    formatted_pv_array = open("formatted_pv_array.txt", "w")

    with open("Photovoltaic array A measurements.csv") as pv_array:
        next(pv_array)
        for line in pv_array:
            line = to_float(line.split(","))
            date_time, g_ap, g_rp, *_ = line

            if g_ap in ["", "\n"]:
                g_ap = prev_val

            prev_val = g_ap

            formatted_pv_array.write(f"{date_time},{g_ap}\n")


def get_pv_array_data_by_date(filter_date):
    with open("formatted_pv_array.txt") as pv_array:
        pv_array_time = open("formatted_pv_array_time.txt", "w")
        pv_array_power = open("formatted_pv_array_power.txt", "w")
        for line in pv_array:
            date_time, power = line.split(",")
            if filter_date in date_time:
                _, time = date_time.split(" ")
                time = f'"{time}"\n'
                pv_array_time.write(time)
                pv_array_power.write(power)


def calc_prob(data, point):
    """points_num = len(set(data))
    prob_list, rang = np.histogram(data, bins=points_num)

    start = rang[0]
    for index, end in enumerate(rang[1:]):
        if start <= point <= end:
            prob = prob_list[index]
            break

        start = end
    return prob / points_num"""
    return data.count(point) / len(data)


def calc_entr(data, prob_filename, entr_filename):
    prob_lst = []
    entr_lst = []

    prob_file = open(f"{prob_filename}.txt", "w")
    entr_file = open(f"{entr_filename}.txt", "w")

    for index in range(0, len(data) // 60):
        print(index)
        print(data[index * 60: (index+1) * 60])
        sum_ = sum(data[index * 60: (index + 1) * 60])
        print(sum_)
        for power in data[index * 60: (index + 1) * 60]:
            prob_lst.append(power / sum_)
        print(prob_lst[-60:])
        print()
        entr = sum([-prob * np.emath.log(prob) for prob in prob_lst[-60::]])
        entr_lst.extend([entr] * 60)

    print(prob_lst)

    for index in range(len(prob_lst)):
        prob_file.write(f"{prob_lst[index]}\n")
        entr_file.write(f"{entr_lst[index]}\n")

    """buff = []

    for i in entr_lst:
        if i not in buff:
            buff.append(i)
    [print(i) for i in buff]
    """

def filter_data(timevals, data, time_filename, data_filename):
    new_timevals = []
    new_data = []

    for index, dat in enumerate(data):
        if dat > 0:
            new_data.append(dat)
            new_timevals.append(timevals[index])

    with open(f"{time_filename}.txt", "w") as f:
        for time in new_timevals:
            f.write(time)

    with open(f"{data_filename}.txt", "w") as f:
        for dat in new_data:
            f.write(f'{dat}\n')


# utils
def to_float(iterbales):
    res = []
    for iterable in iterbales:
        try:
            res.append(float(iterable))
        except ValueError:
            if iterable in ("?", "\n"):
                res.append(0)
            else:
                res.append(iterable)
    return res


def main():
    # get_household_data_by_date("25/11/2010")
    # process_household_data()
    # process_pv_array_data()
    # get_pv_array_data_by_date("2019-05-05")

    with open("formatted_power_file.txt", "r") as data_file:
        data = [float(i.strip("\n")) for i in data_file]
        calc_entr(data, "prob_inp_ideal", "entr_inp_ideal")


    with open("formatted_pv_array_power.txt", "r") as data_file:
        data = [float(i.strip("\n")) for i in data_file]
        f = open("formatted_pv_array_time.txt", "r")
        timevals = f.readlines()
        filter_data(timevals, data, "filtered_pv_array_time", "filtered_pv_array_power")

    print()
    with open("filtered_pv_array_power.txt", "r") as data_file:
        data = [float(i.strip("\n")) for i in data_file]
        calc_entr(data, "prob_inp", "entr_inp")

    print()
    for i in range(0, len(timevals) // 60 + 1):
        print(len(timevals[i * 60: (i + 1) * 60]), timevals[i * 60: (i + 1) * 60])

if __name__ == "__main__":
    main()

