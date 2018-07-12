import numpy


def parse_data(path):
    input = numpy.array()
    output = numpy.array()
    input_size = 0
    output_size = 0
    lines = [line.rstrip('\n') for line in open(path)]
    first = True
    for line in lines:
        if first:
            first = False
            raw_data = line.split(',', 1)
            input_size = raw_data[0]
            output_size = raw_data[1]
        else:
            raw_data = line.split(',', 1)
            reading_input = True
            for item in raw_data:
                if item == "-":
                    reading_input = False
                else:
                    if reading_input:
                        numpy.append(input, float(item))
                    else:
                        numpy.append(output, float(item))
    return input, output, input_size, output_size
