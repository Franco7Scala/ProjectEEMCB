import sys
import Engine


if __name__ == '__main__':
    """param [1] path training set
             [2] path testing set
             [3] epochs
             [4] batch size"""
    path_training_set = sys.argv[1]
    path_test_set = sys.argv[2]
    epochs = sys.argv[3]
    batch_size = sys.argv[4]
    Engine.evaluate(path_training_set, path_test_set, epochs, batch_size)
