import numpy 
import random
import knn
import Parser
import Support
import TrainElement


def calculate_weights(train_elements):
    # calculating weights
    for i in range(len(set_training_big_i)):
        # calculate weights
        pass
    return None

if __name__ == '__main__':
    best_k = 1
    weighted = False
    nearest_found = False
    path_base_neighbors = ""
    path_saving_weights = ""

    # loading data
    path_training_set = ""
    path_test_set = ""

    set_training_i, set_training_o, input_size, _ = Parser.parse_data(path_training_set, 0)
    set_test_i, set_test_o, _, _ = Parser.parse_data(path_test_set, 0)

    set_training_big_i = set_training_i[1:-200]
    set_training_little_i = set_training_i[-200:0]
    set_training_big_o = set_training_o[1:-200]
    set_training_little_o = set_training_o[-200:0]

    quantity_neighbors = 500

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
                for index_lines in range(len(neighbors_i)):
                    for index_values in range(input_size):
                        file.write(str(neighbors_i[index_lines][index_values]) + " ")
                    file.write("= " + str(neighbors_o[index_lines][0]) + "\n")

        else:
            # loading neighbors
            neighbors_i, neighbors_o, _, _ = Parser.parse_data(path_base_neighbors + "/neighbors_" + str(i) + ".txt", 0)

        train_elements.append(TrainElement(current_input, current_output, neighbors_i, neighbors_o))

    # calculating weights
    weights = calculate_weights(train_elements)
    # printing weights
    Support.colored_print(weights, "blue")
    # saving weights
    with open(path_saving_weights, 'a') as file:
        for index_values in range(len(weights)):
            file.write(str(weights[index_values]) + " ")

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











# m denotes the number of examples here, not the number of features
def gradient_descent(x, y, theta, alpha, m, numIterations):
    x_trans = x.transpose()
    for i in range(0, numIterations):
        hypothesis = numpy.dot(x, theta)
        loss = hypothesis - y
        # avg cost per example (the 2 in 2*m doesn't really matter here.
        # But to be consistent with the gradient, I include it)
        cost = numpy.sum(loss ** 2) / (2 * m)
        print("Iteration %d | Cost: %f" % (i, cost))
        # avg gradient per example
        gradient = numpy.dot(x_trans, loss) / m
        # update
        theta = theta - alpha * gradient
    return theta


def gen_data(num_points, bias, variance):
    x = numpy.zeros(shape=(num_points, 2))
    y = numpy.zeros(shape=num_points)
    # basically a straight line
    for i in range(0, num_points):
        # bias feature
        x[i][0] = 1
        x[i][1] = i
        # our target variable
        y[i] = (i + bias) + random.uniform(0, 1) * variance
    return x, y

# gen 100 points with a bias of 25 and 10 variance as a bit of noise
x, y = gen_data(100, 25, 10)
m, n = numpy.shape(x)
numIterations = 100000
alpha = 0.0005
theta = numpy.ones(n)
theta = gradient_descent(x, y, theta, alpha, m, numIterations)
print(theta)








