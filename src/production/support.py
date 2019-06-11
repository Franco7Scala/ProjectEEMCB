# -*- coding: utf-8 -*-
import holidays
import sys


BASE_PATH_NATIONS = "/Users/francesco/Desktop/Cose da Sistemare/test_p/"


def colored_print(text, color):
    if color == "yellow":
        code_color = '\033[93m'
    elif color == "blue":
        code_color = '\033[94m'
    elif color == "green":
        code_color = '\033[92m'
    elif color == "red":
        code_color = '\033[91m'
    elif color == "pink":
        code_color = '\033[95m'
    else:
        code_color = ''
    print code_color + str(text) + '\033[0m'


def print_progress_bar (iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    if iteration == total:
        print()


def calculate_relative_error(real_output, expected_output):
    if real_output != 0:
        return abs((real_output - expected_output) / real_output)
    else:
        return abs((real_output - expected_output) / (real_output + 0.0001))


def is_business_day(date, nation):
    if nation == "FR":
        nation = "FRA"

    return date not in holidays.CountryHoliday(nation)
