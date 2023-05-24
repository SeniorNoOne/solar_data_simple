from classes.file_processor import FileProcessor
from classes.utils import copy_files, make_dir, input_calc, output_calc
from config import GRAPH_CONFIGS


# Equivalent res constants
VOLTAGE = 100
CUT_FACTOR = 0.15


def graph_1():
    # Graph 1
    # Real SP data
    graph_conf = GRAPH_CONFIGS["graph_1"]
    make_dir(graph_conf.path)

    file = FileProcessor(graph_conf.filename, dt_format=graph_conf.dt_format,
                         delimiter=graph_conf.delimiter)
    file.drop_col_from_data(graph_conf.cols_to_drop)
    file.filter_by_date(graph_conf.dt_col, ["2019-04-29", "2019-04-30"])
    file.shift_date("photovoltaic_measurement_timestamp", hours=2)
    file.filter_by_date(graph_conf.dt_col, ["2019-04-29"])
    file.convert_data()
    file.filter_by_value(graph_conf.data_col, min_val=0.1)
    file.preview()
    file.write_col_in_file(graph_conf.dt_col, graph_conf.path + "time_vals_1.txt")
    file.write_col_in_file(graph_conf.data_col, graph_conf.path + "data_vals_1.txt")
    file.write_data_in_file(graph_conf.output_filename)


def graph_2():
    # Graph 2
    # Real SP data
    # NOTE THAT ALL DATA WERE OBTAINED MANUALLY
    graph_conf = GRAPH_CONFIGS["graph_2"]
    make_dir(graph_conf.path)


def graph_3():
    # Graph 3
    # Real load data
    graph_conf = GRAPH_CONFIGS["graph_3"]
    make_dir(graph_conf.path)

    file = FileProcessor(graph_conf.filename, dt_format=graph_conf.dt_format,
                         delimiter=graph_conf.delimiter)
    file.drop_col_from_data(graph_conf.cols_to_drop)
    file.join_columns(["Date", "Time"], "Datetime", delimiter=" ")
    file.filter_by_date("Datetime", ["24/11/2010", "23/11/2010"])
    file.filter_by_date("Datetime", ["24/11/2010"])
    file.convert_data()
    file.write_col_in_file("Datetime", graph_conf.path + "time_vals_3.txt")
    file.data["Global_active_power"] = [power * 1000 for power in file.data["Global_active_power"]]
    file.preview()
    file.write_col_in_file("Global_active_power", graph_conf.path + "data_vals_3.txt")
    file.write_data_in_file(graph_conf.path + "graph_3.txt")


def graph_4():
    # Graph 4
    # Ideal load data
    # NOTE THAT MATLAB USES DATA FROM GRAPH 3
    graph_conf_prev = GRAPH_CONFIGS["graph_3"]
    graph_conf = GRAPH_CONFIGS["graph_4"]

    make_dir(graph_conf.path)
    copy_files(graph_conf_prev.path, graph_conf.path, file_extension="graph_3.txt")

    file = FileProcessor(graph_conf.path + "graph_3.txt")
    file.split_columns("col3", ["date", "time"], delimiter=" ")
    file.convert_data()
    length = len(file.data["col2"])
    mean_value = sum(file.data["col2"]) / length
    file.data["mean"] = [mean_value] * length
    file.preview()
    file.write_col_in_file("mean", graph_conf.path + "data_vals_4.txt")
    file.write_col_in_file("time", graph_conf.path + "time_vals_4.txt")


def graph_5():
    # Graph 5
    # Input entropy
    # Uses files from Graph 1 and Graph 2
    graph_conf_1 = GRAPH_CONFIGS["graph_1"]
    graph_conf_2 = GRAPH_CONFIGS["graph_2"]
    graph_conf = GRAPH_CONFIGS["graph_5"]
    make_dir(graph_conf.path)
    copy_files(graph_conf_1.path, graph_conf.path, file_extension="graph_1.txt")
    copy_files(graph_conf_2.path, graph_conf.path, file_extension="graph_2.txt")

    r_file = FileProcessor(graph_conf.path + "graph_1.txt", dt_format="%H:%M:%S")
    r_file.convert_data()
    r_file.filter_by_value("col1", 0.1)
    r_file.preview()
    r_file.split_columns("col0", ["date", "time"], delimiter=" ")
    r_file.calc_probability("col1", "time")
    r_file.preview()
    r_file.write_col_in_file("stats_time", graph_conf.path + "inp_real_time_vals.txt")
    r_file.write_col_in_file("entropy", graph_conf.path + "inp_real_entropy.txt")
    r_file.write_col_in_file("probability", graph_conf.path + "inp_real_prob.txt")

    i_file = FileProcessor(graph_conf.path + "graph_2.txt", dt_format="%H:%M")
    i_file.convert_data()
    i_file.calc_probability("col1", "col0")
    i_file.preview()
    i_file.write_col_in_file("stats_time", graph_conf.path + "inp_ideal_time_vals.txt")
    i_file.write_col_in_file("entropy", graph_conf.path + "inp_ideal_entropy.txt")
    i_file.write_col_in_file("probability", graph_conf.path + "inp_ideal_prob.txt")

    i_file.subtract_col("stats_time", "entropy", r_file, "stats_time", "entropy")
    i_file.preview()
    i_file.write_col_in_file("diff_data", graph_conf.path + "inp_diff_entropy.txt")
    i_file.write_col_in_file("diff_time", graph_conf.path + "inp_diff_time_vals.txt")


def graph_6():
    # Graph 6
    # Output entropy
    # Uses files from Graph 3 and Graph 4
    graph_conf_3 = GRAPH_CONFIGS["graph_3"]
    graph_conf_4 = GRAPH_CONFIGS["graph_4"]
    graph_conf = GRAPH_CONFIGS["graph_6"]
    make_dir(graph_conf.path)
    copy_files(graph_conf_3.path, graph_conf.path, file_extension="graph_3.txt")
    copy_files(graph_conf_4.path, graph_conf.path, file_extension="vals_4.txt")

    r_file = FileProcessor(graph_conf_4.path + "graph_3.txt", dt_format="%H:%M:%S")
    r_file.convert_data()
    r_file.filter_by_value("col2", 0.1)
    r_file.split_columns("col3", ["date", "time"], delimiter=" ")
    r_file.calc_probability("col2", "time")
    r_file.preview()
    r_file.write_col_in_file("stats_time", graph_conf.path + "out_real_time_vals.txt")
    r_file.write_col_in_file("entropy", graph_conf.path + "out_real_entropy.txt")
    r_file.write_col_in_file("probability", graph_conf.path + "out_real_prob.txt")

    i_file_time = FileProcessor(graph_conf.path + "time_vals_4.txt", dt_format="%H:%M:%S")
    i_file_data = FileProcessor(graph_conf.path + "data_vals_4.txt")
    i_file_time.merge_two_to_one(i_file_data)
    i_file_time.convert_data()
    i_file_time.calc_probability("col0_merged", "col0")
    i_file_time.preview()
    i_file_time.write_col_in_file("stats_time", graph_conf.path + "out_ideal_time_vals.txt")
    i_file_time.write_col_in_file("entropy", graph_conf.path + "out_ideal_entropy.txt")
    i_file_time.write_col_in_file("probability", graph_conf.path + "out_ideal_prob.txt")

    i_file_time.subtract_col("stats_time", "entropy", r_file, "stats_time", "entropy")
    i_file_time.preview()
    i_file_time.write_col_in_file("diff_data", graph_conf.path + "out_diff_entropy.txt")
    i_file_time.write_col_in_file("diff_time", graph_conf.path + "out_diff_time_vals.txt")


def graph_7():
    # Graph 7
    # Entropy divergence and relay graph
    # Uses files from Graph 5 and Graph 6
    graph_conf_5 = GRAPH_CONFIGS["graph_5"]
    graph_conf_6 = GRAPH_CONFIGS["graph_6"]
    graph_conf = GRAPH_CONFIGS["graph_7"]
    make_dir(graph_conf.path)
    copy_files(graph_conf_5.path, graph_conf.path, file_extension="inp_diff_time_vals.txt")
    copy_files(graph_conf_5.path, graph_conf.path, file_extension="inp_diff_entropy.txt")
    copy_files(graph_conf_6.path, graph_conf.path, file_extension="out_diff_time_vals.txt")
    copy_files(graph_conf_6.path, graph_conf.path, file_extension="out_diff_entropy.txt")

    inp_file_time = FileProcessor(graph_conf.path + "inp_diff_time_vals.txt", dt_format="%H:%M")
    inp_file_diff = FileProcessor(graph_conf.path + "inp_diff_entropy.txt")
    inp_file_time.merge_two_to_one(inp_file_diff)
    inp_file_time.convert_data()
    inp_file_time.preview()

    out_file_time = FileProcessor(graph_conf.path + "out_diff_time_vals.txt", dt_format="%H:%M:%S")
    out_file_diff = FileProcessor(graph_conf.path + "out_diff_entropy.txt")
    out_file_time.merge_two_to_one(out_file_diff)
    out_file_time.convert_data()
    out_file_time.preview()

    inp_file_time.subtract_col("col0", "col0_merged", out_file_time, "col0", "col0_merged")
    inp_file_time.signum("diff_data", 1, 0.5)
    inp_file_time.preview()
    inp_file_time.write_col_in_file("diff_data", graph_conf.path + "total_entropy_diff.txt")
    inp_file_time.write_col_in_file("diff_time", graph_conf.path + "total_time.txt")
    inp_file_time.write_col_in_file("diff_data_signum", graph_conf.path + "total_step.txt")


def calc_graphs():
    graph_1()
    graph_2()
    graph_3()
    graph_4()
    graph_5()
    graph_6()
    print("Graphs calculated")


def calc_equivalent_res():
    input_calc(VOLTAGE, CUT_FACTOR)
    output_calc(VOLTAGE, CUT_FACTOR)
    print("Res calculated")


if __name__ == "__main__":
    match input("1 - calc graphs\n"
                "2 - calc equivalent res"
                ": "):
        case "1":
            calc_graphs()
        case "2":
            calc_equivalent_res()
        case _:
            print("Wrong input. Try again\n\n")
