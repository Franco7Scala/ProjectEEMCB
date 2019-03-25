import numpy
import knn
import Parser
import Support
from TrainElement import TrainElement


def gradient_descent(train_elements, alpha, numIterations, k, verbose = 0):
    sum_cost = 0
    for j in range(len(train_elements)):
        x = numpy.asarray(train_elements[j].input)
        y = numpy.asarray(train_elements[j].output)
        # m denotes the number of examples here
        m, n = numpy.shape(x)
        theta = numpy.ones(n)
        x_trans = x.transpose()
        for i in range(0, numIterations):
            hypothesis = knn.get_error_estimation_weighted_on_input(train_elements[j].input, theta, train_elements[j].neighbors_i, train_elements[j].neighbors_o, k, False)
            loss = hypothesis - y
            if verbose:
                cost = numpy.sum(loss ** 2) / (2 * m)
                Support.colored_print("Element %d | Iteration %d | Cost: %f" % (j, i, cost), "red")

            # avg gradient per example
            gradient = numpy.dot(x_trans, loss) / m
            # update
            theta = theta - alpha * gradient

        cost = numpy.sum(loss ** 2) / (2 * m)
        sum_cost += cost

    avg_cost = sum_cost/len(train_elements)
    return theta, avg_cost


def calculate_weights(train_elements, k, verbose):
    num_iterations = 100000
    alpha = 0.0005
    theta, cost = gradient_descent(train_elements, alpha, num_iterations, k, verbose)
    return theta, cost


if __name__ == '__main__':
    best_k = 3
    weighted = False
    nearest_found = True
    verbose = True
    path_base_neighbors = "/Users/francesco/Desktop/Cose da Sistemare/out_knn/neighbors"
    path_saving_weights = "/Users/francesco/Desktop/Cose da Sistemare/out_knn/weights"

    # loading data
    path_training_set = "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_wp.txt"
    path_test_set = "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_wp.txt"

    set_training_i, set_training_o, input_size, _ = Parser.parse_data(path_training_set, 0)
    set_test_i, set_test_o, _, _ = Parser.parse_data(path_test_set, 0)

    set_training_big_i = set_training_i[:-20]
    set_training_big_o = set_training_o[:-20]

    set_training_little_i = set_training_i[-20:]
    set_training_little_o = set_training_o[-20:]

    quantity_neighbors = 10

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
            path_saving_neighbors = path_base_neighbors + "/neighbors_" + str(i) + ".txt"
            with open(path_saving_neighbors, 'a') as file:
                file.write(str(neighbors_i[0].size) + "," + str(1) + "," + str(quantity_neighbors) + "\n")
                for index_lines in range(len(neighbors_i)):
                    for index_values in range(input_size):
                        file.write(str(neighbors_i[index_lines][index_values]) + " ")
                    file.write("= " + str(neighbors_o[index_lines][0]) + "\n")

        else:
            # loading neighbors
            neighbors_i, neighbors_o, _, _ = Parser.parse_data(path_base_neighbors + "/neighbors_" + str(i) + ".txt", 0)

        train_element = TrainElement(current_input, current_output, neighbors_i, neighbors_o)
        train_elements.append(train_element)

    if verbose:
        Support.colored_print("Calculating weights...", "yellow")
    # calculating weights
    weights, cost = calculate_weights(train_elements, best_k, verbose)
    # printing weights
    Support.colored_print(weights, "blue")
    Support.colored_print("Cost: " + str(cost), "green")
    # saving weights
    with open(path_saving_weights, 'a') as file:
        for index_values in range(len(weights)):
            file.write(str(weights[index_values]) + " ")

    if verbose:
        Support.colored_print("Testing...", "yellow")

    # testing on test set
    sum_errors = 0
    for i in range(len(set_test_i)):
        # calculating error
        current_input = set_test_i[i]
        error = knn.get_error_estimation_weighted_on_input(current_input, set_training_big_i, set_training_big_o, best_k, weighted)
        # calculating statistics
        sum_errors += abs(error - set_test_o[i][0])

    avg_error = sum_errors / len(set_test_i)
    # printing results
    Support.colored_print("Avg accuracy (absolute error): " + str(avg_error) + "%", "pink")
    Support.colored_print("Completed!", "pink")
