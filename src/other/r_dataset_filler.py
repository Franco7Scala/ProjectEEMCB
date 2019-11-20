import datetime


date = datetime.datetime(2018, 1, 1)

while date < datetime.datetime(2018, 12, 31):
    if date.hour < 23:
        date = date.replace(hour=date.hour + 1)

    else:
        date = date.replace(hour=0)
        try:
            date = date.replace(day=date.day + 1)
        except:
            date = date.replace(day=1)
            date = date.replace(month=date.month + 1)


    line = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2) + ";" + str(date.hour + 1) + ";0;0;0"
    print line


