import numpy


def parse_data(path):
    inputs = numpy.empty()
    outputs = numpy.empty()
    with open(path, "r") as input_file:
        for line in input_file:
            raw_input, raw_output = line.split('=')
            input = numpy.empty()
            for e in enumerate(raw_input.split()):
                numpy.append(input, float(e.strip()))

            output = numpy.empty()
            for e in enumerate(raw_output.split()):
                numpy.append(output, float(e.strip()))

    return inputs, outputs, len(inputs), len(outputs)