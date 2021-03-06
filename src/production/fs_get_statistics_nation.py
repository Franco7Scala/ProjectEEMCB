from __future__ import division
import sys
import os
import nation
import support


if len(sys.argv) == 1 or sys.argv[1] == "help":
    support.colored_print("Usage:\n\t-parameter 1: nation code (string)", "red")
    sys.exit(0)

nation_code = sys.argv[1]

nation = nation.load_nation(nation_code)
files = os.listdir(nation.base_path_datas)
files.sort()
for file in files:
    if "verbose_out" in file:
        verbose_file = nation.base_path_datas + "/" + file
        with open(verbose_file, 'r') as f:
            support.colored_print(f.read(), "blue")
            support.colored_print("----------------------------------------------", "green")

support.colored_print("Completed!", "pink")
