from __future__ import division
import sys
import nation
import support
import warnings
import MySQLdb
import json


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


if len(sys.argv) == 1 or sys.argv[1] == "help":
    support.colored_print("Usage:\n\t-parameter 1: nation code (string)\n\t-parameter 2: verbose (bool)", "red")
    sys.exit(0)

nation_code = sys.argv[1]
verbose = bool(sys.argv[2])

nation = nation.load_nation(nation_code)

# building datasets
# extracting inputs and outputs
# getting datas from database
with open(support.BASE_PATH_RESOURCES + "db.json", "r") as input_file:
    dict = json.load(input_file)

db = MySQLdb.connect(host=dict["host"], user=dict["user"], passwd=dict["password"], db=dict["database"])

columns_name = ["nation_code", "year", "day_in_year", "holiday", "hour", "production_pv", "production_hydro", "production_biomass", "production_wind", "consumption", "transits", "price_oil", "price_gas", "price_carbon", "production_fossil_coal_gas", "production_fossil_gas", "production_fossil_hard_coal", "production_fossil_oil", "production_nuclear", "production_other", "production_waste", "production_lignite", "production_other_renewable", "production_other_geothermal"]
cursor = db.cursor()
columns_to_keep = ""
for input_index in nation.columns_inputs:
    columns_to_keep += columns_name[input_index] + ", "

for output_index in nation.columns_outputs:
    columns_to_keep += columns_name[output_index] + ", "

columns_to_keep = columns_to_keep[:-2]
cursor.execute("SELECT " + columns_to_keep + " FROM production_data WHERE nation_code = '" + nation_code + "'")
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
input_quantity = len(nation.columns_inputs)
output_quantity = len(nation.columns_outputs)
for x in range(0, num_rows):
    row = cursor.fetchone()
    # saving output
    current_output = []
    for output_index in range(0, output_quantity):
        current_output.append(row[input_quantity + output_index])

    outputs.append(current_output)

    # first part of input
    line_rf = ""
    line_wp = ""
    line_wpwl = ""
    line_wpaw = ""
    for input_index in range(0, input_quantity):
        line_rf += str(row[input_index]) + " "
        line_wp += str(row[input_index]) + " "
        line_wpwl += str(row[input_index]) + " "
        line_wpaw += str(row[input_index]) + " "

    # building RF dataset
    line_rf += "="
    for output_index in range(0, output_quantity):
        line_rf += " " + str(row[input_quantity + output_index])

    text_file_rf.write(line_rf + "\n")

    # building WP / WPWL dataset
    for output_index in range(0, output_quantity):
        if x < back_time_wp:
            line_wp += str(row[input_quantity + output_index]) + " "
        else:
            line_wp += str(outputs[x - back_time_wp][output_index]) + " "

        if x < back_time_wpwl:
            line_wpwl += str(row[input_quantity + output_index]) + " "
        else:
            line_wpwl += str(outputs[x - back_time_wpwl][output_index]) + " "

    line_wp += "="
    line_wpwl += "="
    for output_index in range(0, output_quantity):
        line_wp += " " + str(row[input_quantity + output_index])
        line_wpwl += " " + str(row[input_quantity + output_index])

    text_file_wp.write(line_wp + "\n")
    text_file_wpwl.write(line_wpwl + "\n")

    # building WPAW dataset
    for amount_days in range(1, 8):
        back_time = back_day * amount_days
        for output_index in range(0, output_quantity):
            if x < back_time:
                line_wpaw += str(row[input_quantity + output_index]) + " "
            else:
                line_wpaw += str(outputs[x - back_time][output_index]) + " "

    line_wpaw += "="
    for output_index in range(0, output_quantity):
        line_wpaw += " " + str(row[input_quantity + output_index])

    text_file_wpaw.write(line_wpaw + "\n")

# close the connection and file stream
db.close()
text_file_rf.close()
text_file_wp.close()
text_file_wpwl.close()
text_file_wpaw.close()
support.colored_print("Completed!", "pink")
