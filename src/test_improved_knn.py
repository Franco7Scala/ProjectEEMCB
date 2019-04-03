import numpy
import knn
import Parser
import Support
from TrainElement import TrainElement


def gradient_descent(train_elements, alpha, numIterations, k, verbose = 0):
    inputs = []
    outputs = []
    for e in range(0, len(train_elements)):
        inputs.append(train_elements[e].input)
        outputs.append(train_elements[e].output)

    x = numpy.asarray(inputs)
    y = numpy.asarray(outputs)
    m, n = numpy.shape(x)
    theta = numpy.ones(n)
    x_trans = x.transpose()
    for i in range(0, numIterations):
        results = []
        for j in range(len(train_elements)):
            results.append(knn.get_error_estimation_weighted_on_input(train_elements[j].input, theta, train_elements[j].neighbors_i, train_elements[j].neighbors_o, k, False))

        hypothesis = numpy.asarray(results)
        loss = hypothesis - y
        if verbose:
            cost = numpy.sum(loss ** 2) / (2 * m)
            Support.colored_print("Iteration %d | Cost: %f" % (i, cost), "red")

        # avg gradient per example
        gradient = numpy.dot(x_trans, loss) / m
        # update
        theta = theta - alpha * gradient

    cost = numpy.sum(loss ** 2) / (2 * m)
    return theta, cost


def calculate_weights(train_elements, k, verbose):
    num_iterations = 1000
    alpha = 0.0005
    theta, cost = gradient_descent(train_elements, alpha, num_iterations, k, verbose)
    return theta, cost


if __name__ == '__main__':
    best_k = 3
    weighted = False
    selected_output = 3

    path_saving_base_neighbors = "/Users/francesco/Desktop/Cose da Sistemare/out_knn/neighbors"
    path_saving_weights = "/Users/francesco/Desktop/Cose da Sistemare/out_knn/weights/weights.txt"

    # loading data
    path_training_set = "/Users/francesco/Desktop/Cose da Sistemare/datas/error/test_sets/test_set_fossil_coal_error.txt"
    path_test_set = "/Users/francesco/Desktop/Cose da Sistemare/datas/error/test_sets/test_set_fossil_coal_error.txt"

    nearest_found = False

    set_training_i, set_training_o, input_size, _ = Parser.parse_data(path_training_set, 0)
    set_test_i, set_test_o, _, _ = Parser.parse_data(path_test_set, 0)

    set_training_big_i = set_training_i[:-20]
    set_training_big_o = set_training_o[:-20]

    set_training_little_i = set_training_i[-20:]
    set_training_little_o = set_training_o[-20:]

    verbose = True
    quantity_neighbors = 5

    if nearest_found:
        if verbose:
            Support.colored_print("Loading neighbors...", "yellow")
    else:
        if verbose:
            Support.colored_print("Searching neighbors...", "yellow")

    train_elements = []
    for i in range(len(set_training_little_i)):
        current_input = set_training_little_i[i]
        current_output = set_training_little_o[i]
        if not nearest_found:
            # finding neighbors
            neighbors_i, neighbors_o = knn.find_k_neighbors(current_input, set_training_big_i, set_training_big_o, quantity_neighbors)
            # saving neighbors
            path_saving_neighbors = path_saving_base_neighbors + "/neighbors_" + str(i) + ".txt"
            with open(path_saving_neighbors, 'a') as file:
                file.write(str(neighbors_i[0].size) + "," + str(1) + "," + str(quantity_neighbors) + "\n")
                for index_lines in range(len(neighbors_i)):
                    for index_values in range(input_size):
                        file.write(str(neighbors_i[index_lines][index_values]) + " ")
                    file.write("= " + str(neighbors_o[index_lines][0]) + "\n")

        else:
            # loading neighbors
            neighbors_i, neighbors_o, _, _ = Parser.parse_data(path_saving_base_neighbors + "/neighbors_" + str(i) + ".txt", 0)

        train_element = TrainElement(current_input, current_output[0], neighbors_i, neighbors_o)
        train_elements.append(train_element)

    if verbose:
        Support.colored_print("Calculating weights...", "yellow")
    # calculating weights
    weights, cost = calculate_weights(train_elements, best_k, verbose)
    # printing weights
    Support.colored_print(weights, "blue")
    Support.colored_print("Cost: " + str(cost), "green")
    # saving weights
    with open(path_saving_weights, 'w') as file:
        for index_values in range(len(weights)):
            file.write(str(weights[index_values]) + " ")

    if verbose:
        Support.colored_print("Testing...", "yellow")

    # testing on test set
    sum_errors = 0
    for i in range(len(set_test_i)):
        percentage = (float(i) / float(len(set_test_i))) * 100
        Support.print_progress_bar(i, len(set_test_i), prefix='Progress:', suffix='Complete', length=50)
        # calculating error
        current_input = set_test_i[i]
        error = knn.get_error_estimation_weighted_on_input(current_input, weights, set_training_big_i, set_training_big_o, best_k, weighted)
        # calculating statistics
        sum_errors += abs(error - set_test_o[i][0])

    Support.colored_print("\rResults:", "yellow")
    avg_error = sum_errors / len(set_test_i)
    # printing results
    Support.colored_print("Avg accuracy (absolute error): %.2lf %%" % (avg_error * 100), "pink")
    Support.colored_print("Completed!", "pink")
