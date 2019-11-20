# -*- coding: utf-8 -*-
import csv
import datetime

path_output_file = "/Users/francesco/Desktop/aaa.txt"
path_input_files = { "GER": "/Users/francesco/Downloads/Volumes_Update/auction_spot_volumes_germany_luxembourg_2019(1).csv",
                     "SWI": "/Users/francesco/Downloads/Volumes_Update/auction_spot_volumes_switzerland_2019(1).csv",
                     "FRA": "/Users/francesco/Downloads/Volumes_Update/auction_spot_volumes_france_2019(1).csv" }

all_lines = {}

for current_nation in sorted(path_input_files.keys()):
    path_input_file = path_input_files[current_nation]

    with open(path_input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        firsts = 2
        for row in csv_reader:
            if firsts > 0:
                firsts = firsts - 1

            else:
                hour = 0
                for i in range(1, len(row) - 1):
                    if i != 4:
                        date = datetime.datetime(int(row[0][6:10]), int(row[0][3:5]), int(row[0][0:2]))
                        date = date.replace(hour=hour)
                        hour += 1
                        if row[i] == "":
                            value = 0
                        else:
                            value = float(row[i])

                        if date not in all_lines:
                            all_lines[date] = {current_nation: value}

                        else:
                            all_lines[date][current_nation] = value

with open(path_output_file, "w") as output_file:
    first_line = "Date;Hour;"
    for nation in sorted(path_input_files):
        first_line += nation + ";"

    output_file.write(first_line[:-1] + "\n")
    for key in sorted(all_lines.keys()):
        line = str(key.year) + str(key.month).zfill(2) + str(key.day).zfill(2) + ";" + str(key.hour + 1) + ";"
        for nation in sorted(path_input_files):
            if nation in all_lines[key]:
                line += str(all_lines[key][nation]) + ";"
            else:
                line += "0.0;"

        output_file.write(line[:-1] + "\n")