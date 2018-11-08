import NeuralNetwork
import Parser
import Support


def evaluate(path_network, input):
    Support.colored_print("Loading neural network...", "blue")
    neural_network = NeuralNetwork.NeuralNetwork()
    neural_network.load(path_network)
    Support.colored_print("Evaluating...", "blue")
    result = neural_network.evaluate(input)
    Support.colored_print(result, "pink")


def train(path_training_set, path_target_set, path_output, epochs, batch_size, load, output_selected=-1):
    # keeping data
    Support.colored_print("Loading training set...", "green")
    training_input, training_output, input_size, output_size = Parser.parse_data(path_training_set)
    if output_selected != -1:
        training_output = training_output[:, output_selected]
        output_size = 1
    Support.colored_print("Loading test set...", "green")
    test_input, test_output, x, y = Parser.parse_data(path_target_set)
    if output_selected != -1:
        test_output = test_output[:, output_selected]
        output_size = 1
    # building neural network
    Support.colored_print("Building neural network...", "green")
    neural_network = NeuralNetwork.NeuralNetwork()
    if load == 1:
        neural_network.load(path_output)
    else:
        neural_network.create(input_size, output_size)
    # training
    Support.colored_print("Training...", "green")
    if output_selected != -1:
        neural_network.train(training_input, training_output, test_input, test_output, epochs=epochs, batch_size=batch_size, verbose=1, saving_path=path_output)
    else:
        neural_network.train(training_input, training_output, test_input, test_output, epochs=epochs, batch_size=batch_size, verbose=1)
    # saving neural network
    Support.colored_print("Saving...", "green")
    neural_network.save(path_output)
    Support.colored_print("Finished!", "green")
