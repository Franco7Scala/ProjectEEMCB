import numpy
import Support


def parse_data(path):
    first = True
    second = True
    k = 0
    with open(path, "r") as inputFile:
        for line in inputFile:
            if first:
                first = False
                tokens = line.split(",")
                input_size = int(tokens[0])
                output_size = int(tokens[1])
                samples_size = int(tokens[2])
                inputs = numpy.zeros((samples_size, input_size))
                outputs = numpy.zeros((samples_size, output_size))
            elif second:
                second = False
                Support.colored_print("Parameters: ", "blue")
                Support.colored_print(line, "blue")
            else:
                tokens = line.split(" ")
                i = 0
                j = 0
                reading_input = True
                for token in tokens:
                    if token == "=":
                        reading_input = False
                    else:
                        if reading_input:
                            inputs[k][i] = float(token)
                            i += 1
                        else:
                            outputs[k][j] = float(token)
                            j += 1
                k += 1
    return inputs, outputs, input_size, output_size

