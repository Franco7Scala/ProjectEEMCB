import Support
import Parser
import knn
import numpy
from sklearn.externals import joblib


if __name__ == '__main__':
    verbose = False
    weighted = False
    index_output_prediction = 0
    k_to_try = 100
    path_model = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/all/fossil_oil.joblib"
    path_training_set_error = "/Users/francesco/Desktop/Cose da Sistemare/datas/error/training_sets/training_set_fossil_oil_error.txt"
    path_test_set_prediction = "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_wpwl.txt"
    path_test_set_error = "/Users/francesco/Desktop/Cose da Sistemare/datas/error/test_sets/test_set_fossil_oil_error.txt"

    model = joblib.load(path_model)

    training_set_error_input, training_set_error_output, _, _ = Parser.parse_data(path_training_set_error, 0)
    test_set_prediction_input, test_set_prediction_output, _, _ = Parser.parse_data(path_test_set_prediction, 0)
    _, test_set_error_output, _, _ = Parser.parse_data(path_test_set_error, 0)

    best_k = 0
    avg_accuracy_best_k = float("inf")
    all_avg_values = []

    for current_k in range(51, (k_to_try + 1)):
        Support.colored_print("Current k: " + str(current_k), "blue")
        sum_errors = 0
        for i in range(0, len(test_set_prediction_input)):
            current_input = test_set_prediction_input[i]
            prediction = model.predict((numpy.asarray(current_input)).reshape(1, -1))
            if verbose:
                Support.colored_print("Model output: " + str(prediction), "blue")
                Support.colored_print("Real output: " + str(test_set_prediction_output[i][index_output_prediction]), "blue")

            error = knn.get_error_estimation(current_input, training_set_error_input, training_set_error_output, current_k, weighted)
            if verbose:
                Support.colored_print("Knn based error: " + str(error), "red")
                Support.colored_print("Real error: " + str(test_set_error_output[i][0]), "red")
                Support.colored_print("Absolute error knn estimation: " + str(abs(error - test_set_error_output[i][0])), "green")

            sum_errors += abs(error - test_set_error_output[i][0])

        avg_error = sum_errors/len(test_set_prediction_input)
        all_avg_values.append(avg_error)
        if avg_error < avg_accuracy_best_k:
            best_k = current_k
            avg_accuracy_best_k = avg_error

    Support.colored_print("Best k value: " + str(best_k) + " with avg accuracy (absolute error): " + str(avg_accuracy_best_k) + "%", "pink")
    Support.colored_print(str(all_avg_values), "red")
    Support.colored_print("Completed!", "pink")
