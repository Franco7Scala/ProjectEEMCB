import Support
import Parser
import knn
import numpy
from sklearn.externals import joblib


if __name__ == '__main__':
    verbose = True
    index_output_prediction = 3
    k_to_try = 50
    path_training_set_prediction = "/Users/francesco/Desktop/Cose da Sistemare/datas/ds/training_set_wp.txt"
    path_test_set_prediction = "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_wp.txt"

    training_set_input, training_set_output, _, _ = Parser.parse_data(path_training_set_prediction, 0)
    test_set_input, test_set_output, _, _ = Parser.parse_data(path_test_set_prediction, 0)

    best_k = 0
    best_k_weighted = 0
    avg_accuracy_best_k = float("inf")
    avg_accuracy_best_k_weighted = float("inf")
    all_avg_values = []
    all_avg_values_weighted = []

    for current_k in range(1, (k_to_try + 1)):
        Support.colored_print("Current k: " + str(current_k), "blue")
        sum_relative_error = 0
        sum_relative_error_weighted = 0
        for i in range(0, len(test_set_input)):
            current_input = test_set_input[i]
            current_output = test_set_output[i][index_output_prediction]
            prediction = knn.get_error_estimation(current_input, training_set_input, training_set_output, current_k, False)
            prediction_weighted = knn.get_error_estimation(current_input, training_set_input, training_set_output, current_k, True)
            if verbose:
                Support.colored_print("Real output: " + str(current_output), "green")
                Support.colored_print("Knn output: " + str(prediction), "red")
                Support.colored_print("Knn weighted output: " + str(prediction_weighted), "red")

            if prediction == 0:
                prediction = 0.0001

            if prediction_weighted == 0:
                prediction_weighted = 0.0001

            sum_relative_error += abs((prediction - current_output) / prediction)
            sum_relative_error_weighted += abs((prediction_weighted - current_output) / prediction_weighted)

        avg_error = sum_relative_error/len(test_set_input)
        avg_error_weighted = sum_relative_error_weighted/len(test_set_input)

        all_avg_values.append(avg_error)
        all_avg_values_weighted.append(avg_error_weighted)

        if avg_error < avg_accuracy_best_k:
            best_k = current_k
            avg_accuracy_best_k = avg_error

        if avg_error_weighted < avg_accuracy_best_k_weighted:
            best_k_weighted = current_k
            avg_accuracy_best_k_weighted = avg_error_weighted

    Support.colored_print("Best k value: " + str(best_k) + " with avg accuracy (relative error): " + str(avg_accuracy_best_k * 100) + "%", "pink")
    Support.colored_print("Best k weighted value: " + str(best_k_weighted) + " with avg accuracy (relative error): " + str(avg_accuracy_best_k_weighted * 100) + "%", "pink")

    Support.colored_print("Values: " + str(all_avg_values), "red")
    Support.colored_print("Weighted values: " + str(all_avg_values_weighted), "red")
    Support.colored_print("Completed!", "pink")
