import sys
import Engine
import numpy


if __name__ == '__main__':
    """param [1] path neural network
             [2] input"""
    path_network = sys.argv[1]
    raw_data = sys.argv[2].split(' ')
    data = numpy.empty([1, int(sys.argv[3])])
    for item in raw_data:
        numpy.append(data, float(item))
    Engine.evaluate(path_network, data)
