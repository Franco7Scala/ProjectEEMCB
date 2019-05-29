from __future__ import division
import sys
import Nation
import support
import warnings
import MySQLdb
import json


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


if len(sys.argv) == 1 or sys.argv[1] == "help":
    support.colored_print("Usage:\n\t-parameter 1: nation id (int)\n\t-parameter 2: verbose (bool)", "red")
    sys.exit(0)

nation_id = sys.argv[1]
verbose = bool(sys.argv[2])

nation = Nation.load_nation(nation_id)

# building datasets
types = ["rf", "wp", "wpwl", "wpaw"]
for type in types:
    # extracting inputs and outputs
    # getting datas from database
    with open(support.BASE_PATH_NATIONS + "/db.json", "r") as input_file:
        dict = json.load(input_file)

    db = MySQLdb.connect(host=dict["host"],
                         user=dict["user"],
                         passwd=dict["password"],
                         db=dict["database"])

    cursor = db.cursor()
    indexes_to_keep = ""
    for input_index in nation.indexes_inputs:
        indexes_to_keep += str(input_index) + ", "

    indexes_to_keep = indexes_to_keep[:-1]
    cursor.execute("SELECT " + indexes_to_keep + " FROM production_data")
    # get the number of rows in the result set
    num_rows = cursor.rowcount
    raw_dataset = ""

    if type == "rf":
        dataset_name = nation.path_training_set_prediction_rf
        for x in range(0, num_rows):
            row = cursor.fetchone()
            line = ""
            for input_index in len(nation.indexes_inputs):
                line += str(row[input_index]) + " "

            line += "="
            for output_index in len(nation.indexes_outputs):
                line += " " + str(row[output_index + len(nation.indexes_inputs)])

            raw_dataset += line

    elif type == "wp" or type == "wpwl":
        outputs = []
        if type == "wp":
            dataset_name = nation.path_training_set_prediction_wp
            back_time = 24
        else:
            dataset_name = nation.path_training_set_prediction_wpwl
            back_time = 24 * 7

        outputs = []
        for x in range(0, num_rows):
            row = cursor.fetchone()
            # saving output
            current_output = []
            for output_index in nation.indexes_outputs:
                current_output.append(row[output_index])
            outputs.append(current_output)

            line = ""
            for input_index in len(nation.indexes_inputs):
                line += str(row[input_index]) + " "

            for output_index in nation.indexes_outputs:
                if x < back_time:
                    line += str(row[output_index + len(nation.indexes_inputs)]) + " "
                else:
                    line += str(outputs[x - back_time][output_index]) + " "

            line += "="
            for output_index in len(nation.indexes_outputs):
                line += " " + str(row[output_index + len(nation.indexes_inputs)])

            raw_dataset += line

    elif type == "wpaw":
        dataset_name = nation.path_training_set_prediction_wpaw
        back_day = 24

        outputs = []
        for x in range(0, num_rows):
            row = cursor.fetchone()
            # saving output
            current_output = []
            for output_index in nation.indexes_outputs:
                current_output.append(row[output_index])
            outputs.append(current_output)
            line = ""
            for input_index in len(nation.indexes_inputs):
                line += str(row[input_index]) + " "

            for amount_days in range(1, 8):
                back_time = back_day * amount_days
                for output_index in nation.indexes_outputs:
                    if x < back_time:
                        line += str(row[output_index + len(nation.indexes_inputs)]) + " "
                    else:
                        line += str(outputs[x - back_time][output_index]) + " "

            line += "="
            for output_index in len(nation.indexes_outputs):
                line += " " + str(row[output_index + len(nation.indexes_inputs)])

            raw_dataset += line

    # close the connection
    db.close()
    # saving dataset
    with open(nation.base_path_datas + dataset_name, "w") as text_file:
        text_file.write(raw_dataset)

support.colored_print("Completed!", "pink")














######################## BKP
# filling inputs
    raw_dataset = ""
    if type == "rf":
        dataset_name = nation.path_training_set_prediction_rf
        for index in range(0, len(raw_inputs)):
            current_input = raw_inputs[index]
            current_output = raw_outputs[index]
            line = ""
            for input_index in nation.indexes_inputs:
                line += str(current_input[input_index]) + " "

            line += "="
            for output_index in nation.indexes_outputs:
                line += " " + str(current_output[output_index])

            raw_dataset += line

    elif type == "wp" or type == "wpwl":
        if type == "wp":
            dataset_name = nation.path_training_set_prediction_wp
            back_time = 24
        else:
            dataset_name = nation.path_training_set_prediction_wpwl
            back_time = 24 * 7

        for index in range(0, len(raw_inputs)):
            current_input = raw_inputs[index]
            current_output = raw_outputs[index]
            line = ""
            for input_index in nation.indexes_inputs:
                line += str(current_input[input_index]) + " "

            for output_index in nation.indexes_outputs:
                if index < back_time:
                    line += str(raw_outputs[index][output_index]) + " "
                else:
                    line += str(raw_outputs[index - back_time][output_index]) + " "

            line += "="
            for output_index in nation.indexes_outputs:
                line += " " + str(current_output[output_index])

            raw_dataset += line

    elif type == "wpaw":
        dataset_name = nation.path_training_set_prediction_wpaw
        back_day = 24
        for index in range(0, len(raw_inputs)):
            current_input = raw_inputs[index]
            current_output = raw_outputs[index]
            line = ""
            for input_index in nation.indexes_inputs:
                line += str(current_input[input_index]) + " "

            for amount_days in range(1, 8):
                back_time = back_day * amount_days
                for output_index in nation.indexes_outputs:
                    if index < back_time:
                        line += str(raw_outputs[index][output_index]) + " "
                    else:
                        line += str(raw_outputs[index - back_time][output_index]) + " "

            line += "="
            for output_index in nation.indexes_outputs:
                line += " " + str(current_output[output_index])

            raw_dataset += line
