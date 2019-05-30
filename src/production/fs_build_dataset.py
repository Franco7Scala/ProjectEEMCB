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


#if len(sys.argv) == 1 or sys.argv[1] == "help":
  #  support.colored_print("Usage:\n\t-parameter 1: nation id (int)\n\t-parameter 2: verbose (bool)", "red")
  #  sys.exit(0)

#nation_id = sys.argv[1]
#verbose = bool(sys.argv[2])

nation_id = 1
verbose = True

nation = Nation.load_nation(nation_id)

# building datasets
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
    indexes_to_keep += str(int(input_index)) + ", "

for output_index in nation.indexes_outputs:
    indexes_to_keep += str(int(output_index)) + ", "

indexes_to_keep = indexes_to_keep[:-2]
cursor.execute("SELECT " + indexes_to_keep + " FROM production_data")
# get the number of rows in the result set
num_rows = cursor.rowcount

#cleaning old datasets
text_file_rf = open(nation.base_path_datas + nation.path_training_set_prediction_rf, "w")
text_file_wp = open(nation.base_path_datas + nation.path_training_set_prediction_wp, "w")
text_file_wpwl = open(nation.base_path_datas + nation.path_training_set_prediction_wpwl, "w")
text_file_wpaw = open(nation.base_path_datas + nation.path_training_set_prediction_wpaw, "w")

outputs = []
back_time_wp = 24
back_time_wpwl = 24 * 7
back_day = 24
for x in range(0, num_rows):
    row = cursor.fetchone()

    # saving output
    current_output = []
    for output_index in range(0, len(nation.indexes_outputs)):
        current_output.append(len(nation.indexes_inputs) + row[output_index])

    outputs.append(current_output)

    # building RF dataset
    line_rf = ""
    for input_index in range(0, len(nation.indexes_inputs)):
        line_rf += str(row[input_index]) + " "

    line_rf += "="
    for output_index in range(0, len(nation.indexes_outputs)):
        line_rf += " " + str(row[output_index + len(nation.indexes_inputs)])

    text_file_rf.write(line_rf + "\n")

    # building WP / WPWL dataset
    line_wp = ""
    line_wpwl = ""
    for input_index in range(0, len(nation.indexes_inputs)):
        line_wp += str(row[input_index]) + " "
        line_wpwl += str(row[input_index]) + " "

    for output_index in range(0, len(nation.indexes_outputs)):
        if x < back_time_wp:
            line_wp += str(row[output_index + len(nation.indexes_inputs)]) + " "
        else:
            line_wp += str(outputs[x - back_time][output_index]) + " "

        if x < back_time_wpwl:
            line_wpwl += str(row[output_index + len(nation.indexes_inputs)]) + " "
        else:
            line_wpwl += str(outputs[x - back_time][output_index]) + " "

    line_wp += "="
    line_wpwl += "="
    for output_index in range(0, len(nation.indexes_outputs)):
        line_wp += " " + str(row[output_index + len(nation.indexes_inputs)])
        line_wpwl += " " + str(row[output_index + len(nation.indexes_inputs)])

    text_file_wp.write(line_wp + "\n")
    text_file_wpwl.write(line_wpwl + "\n")

    # building WPAW dataset
    line_wpaw = ""
    for input_index in range(0, len(nation.indexes_inputs)):
        line_wpaw += str(row[input_index]) + " "

    for amount_days in range(1, 8):
        back_time = back_day * amount_days
        for output_index in range(0, len(nation.indexes_outputs)):
            if x < back_time:
                line_wpaw += str(row[output_index + len(nation.indexes_inputs)]) + " "
            else:
                line_wpaw += str(outputs[x - back_time][output_index]) + " "

    line_wpaw += "="
    for output_index in range(0, len(nation.indexes_outputs)):
        line_wpaw += " " + str(row[output_index + len(nation.indexes_inputs)])

    text_file_wpaw.write(line_wpaw + "\n")

# close the connection and file stream
db.close()
text_file_rf.close()
text_file_wp.close()
text_file_wpwl.close()
text_file_wpaw.close()
support.colored_print("Completed!", "pink")
