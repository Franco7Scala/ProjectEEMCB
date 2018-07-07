import sys
import Engine
import numpy


if __name__ == '__main__':
    """param [1] path neural network
             [2] input"""
    path_network = sys.argv[1]
    raw_data = sys.argv[2]
    #TODO format data
    data = null
    Engine.evaluate(path_network, data)