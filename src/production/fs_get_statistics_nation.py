from __future__ import division
import sys
import os
import Nation
import support


nation_id = sys.argv[1]

nation = Nation.load_nation(nation_id)

files = os.listdir(nation.path_datas)
files.sort()
for file in files:
    if "verbose_out" in file:
        verbose_file = nation.path_datas + file
        with open(verbose_file, 'r') as f:
            support.colored_print(f.read(), "green")
            support.colored_print("----------------------------------------------", "pink")