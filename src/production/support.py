# -*- coding: utf-8 -*-

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


def calculate_relative_error(real_output, expected_output):
    if real_output != 0:
        return abs((real_output - expected_output) / real_output)
    else:
        return abs((real_output - expected_output) / (real_output + 0.0001))