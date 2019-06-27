import os

local_saving_folder = "/Users/francesco/Desktop/raw_data"








names = os.listdir(local_saving_folder)
for i in range(0, len(names)):
    names[i] = local_saving_folder + "/" + names[i]

for name in names:
    if "." not in name:
        new_names = os.listdir(name)
        for i in range(0, len(new_names)):
            names.append(name + "/" + new_names[i])

    else:
        open(name, 'w').close()

