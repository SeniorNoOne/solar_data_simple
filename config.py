from classes.config_class import GraphConfig


FILES_TO_PROCESS = (
    "Photovoltaic array A measurements.csv",
    "household_power_consumption.txt"
)

FILES_INFO = {
    "Photovoltaic array A measurements.csv": {
        "cols_to_drop": (
            "photovoltaic_measurement_reactive_power",
            "photovoltaic_measurement_global_irradiance_pv_plane",
            "photovoltaic_measurement_temperature_point_1",
            "photovoltaic_measurement_temperature_point_2"
        ),
        "dt_format": "%Y-%m-%d %H:%M:%S",
        "dt_col": "photovoltaic_measurement_timestamp",
        "data_col": "photovoltaic_measurement_active_power",
        "delimiter": ","
    },

    "household_power_consumption.txt": {
        "cols_to_drop": (
            "Global_reactive_power",
            "Voltage",
            "Global_intensity",
            "Sub_metering_1",
            "Sub_metering_2",
            "Sub_metering_3"
        ),
        "dt_format": "%d/%m/%Y %H:%M:%S",
        "dt_col": "Datetime",
        "data_col": "Global_active_power",
        "delimiter": ";"
    },
}

GRAPH_PARAMS = {
    "graph_1": {
        "name": "graph_1",
        "filename": FILES_TO_PROCESS[0],
    },
    "graph_2": {
        "name": "graph_2",
        "filename": FILES_TO_PROCESS[0],
    },
    "graph_3": {
        "name": "graph_3",
        "filename": FILES_TO_PROCESS[1],
    },
    "graph_4": {
        "name": "graph_4",
        "filename": "",
    },
    "graph_5": {
        "name": "graph_5",
        "filename": "",
    },
    "graph_6": {
        "name": "graph_6",
        "filename": "",
    },
    "graph_7": {
        "name": "graph_7",
        "filename": "",
    },
}

GRAPH_CONFIGS = dict()
for graph_name in GRAPH_PARAMS:
    graph_params = GRAPH_PARAMS[graph_name]
    file_params = FILES_INFO.get(GRAPH_PARAMS[graph_name]["filename"], dict())
    GRAPH_CONFIGS[graph_name] = GraphConfig(**graph_params,
                                            **file_params)
