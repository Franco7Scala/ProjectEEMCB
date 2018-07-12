import sys
import Engine


if __name__ == '__main__':
    """param [1] path training set
             [2] path testing set
             [3] path output
             [4] epochs
             [5] batch size"""
    path_training_set = sys.argv[1]
    path_test_set = sys.argv[2]
    path_output = sys.argv[3]
    epochs = sys.argv[4]
    batch_size = sys.argv[5]
    Engine.train(path_training_set, path_test_set, path_output, epochs, batch_size)