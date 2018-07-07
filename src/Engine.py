import NeuralNetwork
import Parser
import Trainer


def evaluate(path_network, input):
    print("Loading neural network...")
    neural_network = NeuralNetwork.NeuralNetwork()
    neural_network.load(path_network)
    print("Evaluating...")
    result = neural_network.evaluate(input)
    print(result)


def train(path_training_set, path_target_set, epochs, batch_size):
    print("Building neural network...")
    neural_network = NeuralNetwork.NeuralNetwork()
    neural_network.create()
    # keeping data
    print("Loading training set...")
    training_data = []
    target_data = []
    training_test_data = []
    target_test_data = []
    training_data = Parser.parse_input(path_training_set)
    target_data = Parser.parse_input(path_target_set)
    # load training
    print("Training...")
    Trainer.train(neural_network, training_data, target_data, training_test_data, target_test_data, epochs=epochs, batch_size=batch_size, verbose=1)
    # saving network
    print("Saving...")
    neural_network.save()
    print("Finished!")
