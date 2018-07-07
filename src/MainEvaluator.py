import sys
import Engine
import numpy


if __name__ == '__main__':
    """param [1] mode evaluation or training
             [2] path training set
             [3] path testing set
             [9] samples quantity
             [10] training quantity
             [11] epochs
             [12] batch size"""
    path_network = sys.argv[1]
    raw_data = sys.argv[2]
    #TODO format data
    data = null
    Engine.evaluate(path_network, data)