import sys
import Engine
import numpy


if __name__ == '__main__':
    """param [1] path neural network
             [2] input"""
    path_network = sys.argv[1]
    raw_data = [float(x) for x in sys.argv[2].split(' ')]
    data = numpy.array(raw_data, dtype=float)
    data = data.reshape(1, len(raw_data))
    Engine.evaluate(path_network, data)