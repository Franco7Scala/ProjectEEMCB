import tuple
import requests
import sys
import pysftp
import os
import warnings
import csv
import support
import json
import bisect
import MySQLdb
import codecs
from datetime import datetime, timedelta
from MySQLdb import IntegrityError


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


if len(sys.argv) == 1 or sys.argv[1] == "help":
    support.colored_print("Usage:\n\t-parameter 1: verbose (bool)", "red")
    sys.exit(0)

verbose = bool(sys.argv[1])

local_saving_folder = support.BASE_PATH_NATIONS + "raw_data"
with open(support.BASE_PATH_RESOURCES + "/extraction.json", "r") as input_file:
    dict = json.load(input_file)

with open(support.BASE_PATH_RESOURCES + "/db.json", "r") as input_file:
    db_dict = json.load(input_file)

# downloading files
# entsoe
if verbose:
    support.colored_print("Downloading data from Entsoe...", "green")

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
with pysftp.Connection(host=dict["sftp_entsoe"]["host"], username=dict["sftp_entsoe"]["user"], password=dict["sftp_entsoe"]["password"], cnopts=cnopts) as sftp:
    entsoe_remote_folders = ["/TP_export/ActualTotalLoad/", "/TP_export/AggregatedGenerationPerType/", "/TP_export/CrossBorderPhysicalFlow/"]
    local_folders = [local_saving_folder + "/TP_export/ActualTotalLoad/", local_saving_folder + "/TP_export/AggregatedGenerationPerType/", local_saving_folder + "/TP_export/CrossBorderPhysicalFlow/"]
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

# deleting unnecessaries files
os.remove(local_folders[0] + str(datetime.now().year) + "_" + str(datetime.now().month) + "_ActualTotalLoad.csv")
os.remove(local_folders[1] + str(datetime.now().year) + "_" + str(datetime.now().month) + "_AggregatedGenerationPerType.csv")
os.remove(local_folders[2] + str(datetime.now().year) + "_" + str(datetime.now().month) + "_CrossBorderPhysicalFlow.csv")

local_folders = [local_saving_folder + "/TP_export/ActualTotalLoad/",
                 local_saving_folder + "/TP_export/AggregatedGenerationPerType/",
                 local_saving_folder + "/TP_export/CrossBorderPhysicalFlow/"]

# macrotrends
if verbose:
    support.colored_print("Downloading data from Macrotrends...", "green")

# crude oil
oil_saving_folder = local_saving_folder + "/oil"
try:
    os.makedirs(oil_saving_folder)
except os.error:
    pass

oil_saving_file = oil_saving_folder + "/csv"
try:
    os.remove(oil_saving_file)
except os.error:
    pass

support.download_from_macrotrends(dict["oil_prices_source"], oil_saving_folder)
local_folders.append(oil_saving_file)

# natural gas
gas_saving_folder = local_saving_folder + "/gas"
try:
    os.makedirs(gas_saving_folder)
except os.error:
    pass

gas_saving_file = gas_saving_folder + "/csv"
try:
    os.remove(gas_saving_file)
except os.error:
    pass

support.download_from_macrotrends(dict["gas_prices_source"], gas_saving_folder)
local_folders.append(gas_saving_file)

# quandl
if verbose:
    support.colored_print("Downloading data from Quandl...", "green")

# carbon
http_request = requests.get(dict["carbon_prices_source"])

with open(local_saving_folder + "/carbon.csv", "w") as carbon_file:
    carbon_file.write(http_request.text)

local_folders.append(local_saving_folder + "/carbon.csv")

# aggregating datas
if verbose:
    support.colored_print("Aggregating datas...", "green")

# getting latest import date
db = MySQLdb.connect(host=db_dict["host"], user=db_dict["user"], passwd=db_dict["password"], db=db_dict["database"])
cursor = db.cursor()
cursor.execute("SELECT MAX(year) FROM production_data")
start_year = cursor.fetchone()[0]
if start_year is None:
    start_date = datetime(2016, 1, 1)
else:
    cursor.execute("SELECT MAX(day_in_year) FROM production_data WHERE year = " + str(start_year))
    day_in_year = cursor.fetchone()[0]
    start_date = datetime(start_year, 1, 1) + timedelta(day_in_year)

to_elaborate = (datetime.now().year - start_date.year) * 12 + datetime.now().month - start_date.month
elaborated = -1
for year in range(start_date.year, datetime.now().year + 1):
    start_month = 1
    end_month = 13
    if year == start_date.year:
        start_month = start_date.month

    if year == datetime.now().year:
        end_month = datetime.now().month

    for month in range(start_month, end_month):
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

                    if int(str(row[3])[14:16]) != 0:
                        continue

                    if not support.double_contains(row[8], dict["nations"]):
                        continue

                    if "CA" in row[7]:
                        continue

                    current_date = datetime(int(row[0]), int(row[1]), int(row[2]))
                    current_tuple = tuple.Tuple()
                    current_tuple.nation = row[8]
                    current_tuple.year = year
                    current_tuple.day_in_year = current_date.timetuple().tm_yday
                    current_tuple.hour = int(str(row[3])[11:13])
                    current_tuple.holiday = support.is_business_day(current_date, current_tuple.nation)
                    current_tuple.date = current_date
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
        with codecs.open(local_folders[1] + str(year) + "_" + str(month) + "_AggregatedGenerationPerType.csv", "rU") as csv_file:
            csv_reader = csv.reader((x.replace('\0', '') for x in csv_file), delimiter='\t')
            first = True
            for row in csv_reader:
                if first:
                    first = False

                else:
                    if len(row) < 8:
                        continue

                    if not support.double_contains(row[8], dict["nations"]):
                        continue

                    if not (int(row[0]) == year and int(row[1]) == month):
                        continue

                    if int(str(row[3])[14:16]) != 0:
                        continue

                    if "CA" not in row[7]:
                        continue

                    current_date = datetime(int(row[0]), int(row[1]), int(row[2]))
                    current_tuple = tuple.Tuple()
                    current_tuple.nation = row[8]
                    current_tuple.year = year
                    current_tuple.day_in_year = current_date.timetuple().tm_yday
                    current_tuple.hour = int(str(row[3])[11:13])
                    current_tuple.holiday = support.is_business_day(current_date, current_tuple.nation)
                    current_tuple.date = current_date
                    # checking if tuple's day already encountered
                    found = False
                    for value in tuples:
                        if value == current_tuple:
                            current_tuple = value
                            found = True
                            break

                    # adding generation type value
                    production_type = str(row[9])
                    consumption_source = 0
                    if str(row[11]) != "":
                        consumption_source = float(row[11])

                    if row[10] != "":
                        if "Fossil Gas" in production_type:
                            current_tuple.production_fossil_gas += float(row[10]) - consumption_source

                        elif "Hydro" in production_type:
                            current_tuple.production_hydro += float(row[10]) - consumption_source

                        elif "Nuclear" in production_type:
                            current_tuple.production_nuclear += float(row[10]) - consumption_source

                        elif "Fossil Oil" in production_type:
                            current_tuple.production_fossil_oil += float(row[10]) - consumption_source

                        elif "Fossil Hard coal" in production_type:
                            current_tuple.production_fossil_hard_coal += float(row[10]) - consumption_source

                        elif "Fossil Brown coal/Lignite" in production_type:
                            current_tuple.production_lignite += float(row[10]) - consumption_source

                        elif "Other" in production_type:
                            current_tuple.production_other += float(row[10]) - consumption_source

                        elif "Biomass" in production_type:
                            current_tuple.production_biomass += float(row[10]) - consumption_source

                        elif "Wind" in production_type:
                            current_tuple.production_wind += float(row[10]) - consumption_source

                        elif "Fossil Coal-derived gas" in production_type:
                            current_tuple.production_fossil_coal_gas += float(row[10]) - consumption_source

                        elif "Waste" in production_type:
                            current_tuple.production_waste += float(row[10]) - consumption_source

                        elif "Other renewable" in production_type:
                            current_tuple.production_other_renewable += float(row[10]) - consumption_source

                        elif "Solar" in production_type:
                            current_tuple.production_pv += float(row[10]) - consumption_source

                        elif "Geothermal" in production_type:
                            current_tuple.production_geothermal += float(row[10]) - consumption_source

                    # saving into list
                    if not found:
                        bisect.insort(tuples, current_tuple)

        # reading file containing transits
        with open(local_folders[2] + str(year) + "_" + str(month) + "_CrossBorderPhysicalFlow.csv") as csv_file:
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

                    if int(str(row[3])[14:16]) != 0:
                        continue

                    if not (support.double_contains(row[8], dict["nations"]) or support.double_contains(row[12], dict["nations"])):
                        continue

                    if "CA" not in row[7] and "CA" not in row[11]:
                        continue

                    current_date = datetime(int(row[0]), int(row[1]), int(row[2]))
                    # tuple in
                    current_tuple_in = tuple.Tuple()
                    current_tuple_in.nation = row[12]
                    current_tuple_in.year = year
                    current_tuple_in.day_in_year = current_date.timetuple().tm_yday
                    current_tuple_in.hour = int(str(row[3])[11:13])
                    current_tuple_in.holiday = support.is_business_day(current_date, current_tuple_in.nation)
                    current_tuple_in.date = current_date
                    # checking if tuple's day already encountered
                    found_in = False
                    for value in tuples:
                        if value == current_tuple_in:
                            current_tuple_in = value
                            found_in = True
                            break

                    # tuple out
                    current_tuple_out = tuple.Tuple()
                    current_tuple_out.nation = row[8]
                    current_tuple_out.year = year
                    current_tuple_out.day_in_year = current_date.timetuple().tm_yday
                    current_tuple_out.hour = int(str(row[3])[11:13])
                    current_tuple_out.holiday = support.is_business_day(current_date, current_tuple_out.nation)
                    current_tuple_out.date = current_date
                    # checking if tuple's day already encountered
                    found_out = False
                    for value in tuples:
                        if value == current_tuple_out:
                            current_tuple_out = value
                            found_out = True
                            break

                    if support.double_contains(current_tuple_in.nation, dict["nations"]):
                        current_tuple_in.transits -= float(row[13])
                        if not found_in:
                            bisect.insort(tuples, current_tuple_in)

                    if support.double_contains(current_tuple_out.nation, dict["nations"]):
                        current_tuple_out.transits += float(row[13])
                        if not found_out:
                            bisect.insort(tuples, current_tuple_out)

        # reading file containing price oil and natural gas
        oil_prices = {}
        gas_prices = {}
        for index in range(3, 5):
            with open(local_folders[index], "r") as input_file:
                with open(local_folders[index] + ".tmp", "w") as output_file:
                    found = False
                    line = input_file.readline()
                    while line:
                        if "date, value" in line:
                            found = True

                        if found:
                            output_file.write(line)

                        line = input_file.readline()

            os.rename(local_folders[index] + ".tmp", local_folders[index])

            with open(local_folders[index]) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                first = True
                for row in csv_reader:
                    if first:
                        first = False

                    else:
                        raw_date = str(row[0]).split('-')
                        current_date = datetime(int(raw_date[0]), int(raw_date[1]), int(raw_date[2]))
                        price = float(row[1])
                        if index == 3:
                            oil_prices[current_date] = price

                        else:
                            gas_prices[current_date] = price

        # reading file containing price carbon
        carbon_prices = {}
        with open(local_folders[5]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first = True
            for row in csv_reader:
                if first:
                    first = False

                else:
                    raw_date = str(str(row[0]).split(' ')[0]).split('-')
                    current_date = datetime(int(raw_date[0]), int(raw_date[1]), int(raw_date[2]))
                    carbon_prices[current_date] = float(row[4])

        # applying prices to tuples
        for value in tuples:
            putted = False
            target_date = value.date
            while not putted:
                price = oil_prices.get(target_date)
                if price is not None:
                    value.price_oil = price
                    putted = True
                else:
                    target_date = target_date - timedelta(days=1)

            putted = False
            target_date = value.date
            while not putted:
                price = gas_prices.get(target_date)
                if price is not None:
                    value.price_gas = price
                    putted = True
                else:
                    target_date = target_date - timedelta(days=1)

            putted = False
            target_date = value.date
            while not putted:
                price = carbon_prices.get(target_date)
                if price is not None:
                    value.price_carbon = price
                    putted = True
                else:
                    target_date = target_date - timedelta(days=1)

        # saving all days in month to db
        query = "INSERT INTO production_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for value in tuples:
            val = (value.nation, value.year, value.day_in_year, value.holiday, value.hour, value.production_pv, value.production_hydro, value.production_biomass, value.production_wind, value.consumption, value.transits, value.price_oil, value.price_gas, value.price_carbon, value.production_fossil_coal_gas, value.production_fossil_gas, value.production_fossil_hard_coal, value.production_fossil_oil, value.production_nuclear, value.production_other, value.production_waste, value.production_lignite, value.production_other_renewable, value.production_geothermal)
            try:
                cursor.execute(query, val)
            except IntegrityError as e:
                print e

        db.commit()

if verbose:
    support.print_progress_bar(100, 100, prefix='Progress:', suffix='Completed', length=50)

# freeing space
if verbose:
    support.colored_print("Freeing space...", "green")
"""
names = os.listdir(local_saving_folder)
for i in range(0, len(names)):
    names[i] = local_saving_folder + "/" + names[i]

for name in names:
    if os.path.isdir(name):
        new_names = os.listdir(name)
        for i in range(0, len(new_names)):
            names.append(name + "/" + new_names[i])

    else:
        open(name, 'w').close()
"""
support.colored_print("Completed!", "pink")
