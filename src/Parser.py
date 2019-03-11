import numpy
import Support


def parse_data(path, verbose = 1):
    first = True
    second = True
    k = 0
    counter = 0
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
                if verbose:
                    Support.colored_print("Parameters: ", "blue")
                    Support.colored_print(line, "blue")
            else:
                counter += 1
                if counter < samples_size:
                    input, output = line.split('=')
                    for i,e in enumerate(input.split()):
                        inputs[k][i] = float(e.strip())

                    for i,e in enumerate(output.split()):
                        outputs[k][i] = float(e.strip())
                    k += 1
                else:
                    break
    return inputs, outputs, input_size, output_size