import tuple
import pysftp
import sys
import os
import warnings
import csv
import datetime
import support
import json
import bisect
import MySQLdb
import codecs


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


if len(sys.argv) == 1 or sys.argv[1] == "help":
    #support.colored_print("Usage:\n\t-parameter 1: verbose (bool)", "red")
    #sys.exit(0)
    pass

#verbose = bool(sys.argv[1])
verbose = True

local_saving_folder = support.BASE_PATH_NATIONS + "raw_data"
with open(support.BASE_PATH_NATIONS + "/extraction.json", "r") as input_file:
    dict = json.load(input_file)

with open(support.BASE_PATH_NATIONS + "/db.json", "r") as input_file:
    db_dict = json.load(input_file)

# downloading files
# entsoe
if verbose:
    support.colored_print("Downloading data from Entsoe...", "green")

'''
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
with pysftp.Connection(host=dict["sftp_entsoe"]["host"], username=dict["sftp_entsoe"]["user"], password=dict["sftp_entsoe"]["password"], cnopts=cnopts) as sftp:
    entsoe_remote_folders = ["/TP_export/ActualTotalLoad/", "/TP_export/ActualGenerationOutputPerUnit/", "/TP_export/TransferCapacitiesAllocatedDaily/"]
    local_folders = [local_saving_folder + "/TP_export/ActualTotalLoad/", local_saving_folder + "/TP_export/ActualGenerationOutputPerUnit/", local_saving_folder + "/TP_export/TransferCapacitiesAllocatedDaily/"]
    for i in range(0, len(entsoe_remote_folders)):
        try:
            os.makedirs(local_folders[i])
        except os.error:
            pass

        with sftp.cd(entsoe_remote_folders[i]):
            data = sftp.listdir()
            for line in data:
                if not os.path.exists(local_folders[i] + line):
                    sftp.get(line, local_folders[i] + line)
'''
local_folders = [local_saving_folder + "/TP_export/ActualTotalLoad/",
                 local_saving_folder + "/TP_export/ActualGenerationOutputPerUnit/",
                 local_saving_folder + "/TP_export/TransferCapacitiesAllocatedDaily/"]

# macrotrends
if verbose:
    support.colored_print("Downloading data from Macrotrends...", "green")
# TODO

# crude oil
local_folders.append(local_saving_folder + "/crude oil.csv")

# natural gas
local_folders.append(local_saving_folder + "/natural-gas-prices-historical-chart.csv")

# sandbag
if verbose:
    support.colored_print("Downloading data from Sandbag...", "green")

local_folders.append(local_saving_folder + "/carbon.csv")

# aggregating datas
if verbose:
    support.colored_print("Aggregating datas...", "green")

to_elaborate = ((datetime.datetime.now().year - 2016) * 12) + datetime.datetime.now().month
elaborated = -1
for year in range(2016, datetime.datetime.now().year + 1):
    for month in range(1, datetime.datetime.now().month):
        elaborated += 1
        if verbose:
            support.print_progress_bar(elaborated, to_elaborate, prefix='Progress:', suffix='Completed', length=50)

        tuples = []
        # reading file containing consumption
        with open(local_folders[0] + str(year) + "_" + str(month) + "_ActualTotalLoad.csv") as csv_file:
            csv_reader = csv.reader((x.replace('\0', '') for x in csv_file), delimiter='\t')
            first = True
            for row in csv_reader:
                if first:
                    first = False

                else:
                    if len(row) == 0:
                        continue

                    if not (int(row[0]) == year and int(row[1]) == month):
                        continue

                    if not row[8] in dict["nations"]:
                        continue

                    current_date = datetime.datetime(int(row[0]), int(row[1]), int(row[2]))
                    current_tuple = tuple.Tuple()
                    current_tuple.nation = row[8]
                    current_tuple.year = year
                    current_tuple.day_in_year = current_date.timetuple().tm_yday
                    current_tuple.hour = int(str(row[3])[11:13])
                    current_tuple.holiday = support.is_business_day(current_date, current_tuple.nation)
                    # checking if tuple's day already encountered
                    found = False
                    for value in tuples:
                        if value == current_tuple:
                            current_tuple = value
                            found = True
                            break

                    current_tuple.consumption += float(row[9])

                    # saving into list
                    if not found:
                        bisect.insort(tuples, current_tuple)

        # reading file containing production
        with open(local_folders[1] + str(year) + "_" + str(month) + "_ActualGenerationOutputPerUnit.csv", "rU") as csv_file:
            csv_reader = csv.reader((x.replace('\0', '') for x in csv_file), delimiter='\t')
            first = True
            for row in csv_reader:
                if first:
                    first = False

                else:
                    print row
                    if len(row) == 0:
                        continue

                    if not (int(row[0]) == year and int(row[1]) == month):
                        continue

                    if not row[8] in dict["nations"]:
                        continue

                    current_date = datetime.datetime(int(row[0]), int(row[1]), int(row[2]))
                    current_tuple = tuple.Tuple()
                    current_tuple.nation = row[8]
                    current_tuple.year = year
                    current_tuple.day_in_year = current_date.timetuple().tm_yday
                    current_tuple.hour = int(str(row[3])[11:13])
                    current_tuple.holiday = support.is_business_day(current_date, current_tuple.nation)
                    # checking if tuple's day already encountered
                    found = False
                    for value in tuples:
                        if value == current_tuple:
                            current_tuple = value
                            found = True
                            break

                    # adding generation type value
                    production_type = str(row[11])
                    if row[12] != "":
                        if "Fossil Gas" in production_type:
                            current_tuple.production_fossil_gas += float(row[12])

                        elif "Hydro" in production_type:
                            current_tuple.production_hydro += float(row[12])

                        elif "Nuclear" in production_type:
                            current_tuple.production_nuclear += float(row[12])

                        elif "Fossil Oil" in production_type:
                            current_tuple.production_fossil_oil += float(row[12])

                        elif "Fossil Hard coal" in production_type:
                            current_tuple.production_fossil_hard_coal += float(row[12])

                        elif "Fossil Brown coal/Lignite" in production_type:
                            current_tuple.production_lignite += float(row[12])

                        elif "Other" in production_type:
                            current_tuple.production_other += float(row[12])

                        elif "Biomass" in production_type:
                            current_tuple.production_biomass += float(row[12])

                        elif "Wind" in production_type:
                            current_tuple.production_wind += float(row[12])

                        elif "Fossil Coal-derived gas" in production_type:
                            current_tuple.production_fossil_coal_gas += float(row[12])

                        elif "Waste" in production_type:
                            current_tuple.production_waste += float(row[12])

                    # saving into list
                    if not found:
                        bisect.insort(tuples, current_tuple)

        # reading file containing transits
        with open(local_folders[2] + str(year) + "_" + str(month) + "_TransferCapacitiesAllocatedDaily.csv") as csv_file:
            csv_reader = csv.reader((x.replace('\0', '') for x in csv_file), delimiter='\t')
            first = True
            for row in csv_reader:
                if first:
                    first = False

                else:
                    if len(row) == 0:
                        continue

                    if not (int(row[0]) == year and int(row[1]) == month):
                        continue

                    if not row[8] in dict["nations"]:
                        continue

                    current_date = datetime.datetime(int(row[0]), int(row[1]), int(row[2]))
                    # tuple in
                    current_tuple_in = tuple.Tuple()
                    current_tuple_in.nation = row[11]
                    current_tuple_in.year = year
                    current_tuple_in.day_in_year = current_date.timetuple().tm_yday
                    current_tuple_in.hour = int(str(row[3])[11:13])
                    current_tuple_in.holiday = support.is_business_day(current_date, current_tuple_in.nation)
                    # checking if tuple's day already encountered
                    found = False
                    for value in tuples:
                        if value == current_tuple_in:
                            current_tuple_in = value
                            found = True
                            break

                    # tuple out
                    current_tuple_out = tuple.Tuple()
                    current_tuple_out.nation = row[15]
                    current_tuple_out.year = year
                    current_tuple_out.day_out_year = current_date.timetuple().tm_yday
                    current_tuple_out.hour = int(str(row[3])[11:13])
                    current_tuple_out.holiday = support.is_busoutess_day(current_date, current_tuple_out.nation)
                    # checking if tuple's day already encountered
                    found = False
                    for value in tuples:
                        if value == current_tuple_out:
                            current_tuple_out = value
                            found = True
                            break

                    if current_tuple_in.nation in dict["nations"]:
                        current_tuple_in.transits += float(row[16])

                    if current_tuple_out.nation in dict["nations"]:
                        current_tuple_out.transits -= float(row[16])

                    # saving into list
                    if not found:
                        bisect.insort(tuples, current_tuple)

        # reading file containing price oil and natural gas
        for index in range(3, 5):
            with open(local_folders[index], "r") as input_file:
                with open(local_folders[index] + ".tmp", "w") as output_file:
                    found = False
                    for line in input_file:
                        if line.strip("\n") == "date, value":
                            found = True

                        if found:
                            output_file.write(line)

            os.rename(local_folders[index] + ".tmp", local_folders[index])
            with open(local_folders[index]) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                first = True
                for row in csv_reader:
                    if first:
                        first = False

                    else:
                        raw_date = str(row[0]).split('-')
                        current_date = datetime.datetime(raw_date[0], raw_date[1], raw_date[2])
                        price = float(row[1])
                        for value in tuples:
                            if value.year == current_date.year and value.day_in_year == current_date.timetuple().tm_yday:
                                if index == 3:
                                    value.price_oil = price

                                else:
                                    value.price_gas = price

        # reading file containing price carbon
        with open(local_folders[5]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first = True
            for row in csv_reader:
                if first:
                    first = False

                else:
                    raw_date = str(str(row[0]).split(' ')[0]).split('-')
                    current_date = datetime.datetime(int(raw_date[0]), int(raw_date[1]), int(raw_date[2]))
                    if len(row) > 2:
                        price = float(row[1] + "." + row[2])
                    else:
                        price = float(row[1])

                    for value in tuples:
                        if value.year == current_date.year and value.day_in_year == current_date.timetuple().tm_yday:
                            value.price_carbon = price


        print len(tuples)
        for value in tuples:
            print value

        # saving all days in month to db
        db = MySQLdb.connect(host=db_dict["host"],
                             user=db_dict["user"],
                             passwd=db_dict["password"],
                             db=db_dict["database"])
        cursor = db.cursor()
        query = "INSERT INTO production_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for value in tuples:
            val = (value.nation, value.year, value.day_in_year, value.holiday, value.hour, value.production_pv, value.production_hydro, value.production_biomass, value.production_wind, value.consumption, value.transits, value.price_oil, value.price_gas, value.price_carbon, value.production_fossil_fossil_coal_gas, value.production_fossil_gas, value.production_fossil_hard_coal, value.production_fossil_oil, value.production_nuclear, value.production_other, value.production_waste, value.production_lignite)
            cursor.execute(query, val)

        db.commit()

if verbose:
    support.print_progress_bar(100, 100, prefix='Progress:', suffix='Completed', length=50)

support.colored_print("Completed!", "pink")
