from datetime import datetime, timedelta

start_date = datetime(2016, 1, 1)
now_date = datetime(2019, 12, 10)

to_elaborate =(now_date.year - start_date.year) * 12 + now_date.month - start_date.month
elaborated = -1
for year in range(start_date.year, now_date.year + 1):
    start_month = 1
    end_month = 13
    if year == start_date.year:
        start_month = start_date.month

    if year == now_date.year:
        end_month = now_date.month

    for month in range(start_month, end_month):
        print(str(month) + " " + str(year))