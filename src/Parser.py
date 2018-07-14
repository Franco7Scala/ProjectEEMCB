import numpy


def parse_data(path):
    input = numpy.array(0)
    output = numpy.array(0)
    input_size = 0
    output_size = 0
    lines = [line.rstrip('\n') for line in open(path)]
    first = True
    for line in lines:
        if first:
            first = False
            raw_data = line.split(',')
            input_size = int(raw_data[0])
            output_size = int(raw_data[1])
        else:
            raw_data = line.split(' ')
            reading_input = True
            for item in raw_data:
                if item == "=":
                    reading_input = False
                else:
                    if reading_input:
                        numpy.append(input, float(item))
                    else:
                        numpy.append(output, float(item))
    return input, output, input_size, output_size

