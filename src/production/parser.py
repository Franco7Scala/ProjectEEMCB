import numpy


def parse_data(path):
    inputs = []
    outputs = []
    with open(path, "r") as input_file:
        for line in input_file:
            raw_input, raw_output = line.split('=')
            input = []
            for _, e in enumerate(raw_input.split()):
                input.append(float(e.strip()))

            output = []
            for _, e in enumerate(raw_output.split()):
                output.append(float(e.strip()))

            inputs.append(input)
            outputs.append(output)

    return numpy.array(inputs), numpy.array(outputs)