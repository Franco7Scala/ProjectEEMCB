import Support
import Parser
import knn
import numpy
from sklearn.externals import joblib


if __name__ == '__main__':
    verbose = False
    path_model = ""
    path_training_set_error = ""
    path_test_set_prediction = ""
    path_test_set_error = ""

    model = joblib.load(path_model)

    training_set_error_input, training_set_error_output, _, _ = Parser.parse_data(path_training_set_error, 0)
    test_set_prediction_input, test_set_prediction_output, _, _ = Parser.parse_data(path_test_set_prediction, 0)
    _, test_set_error_output, _, _ = Parser.parse_data(path_test_set_error, 0)

    best_k = 0
    avg_accuracy_best_k = float("inf")

    for current_k in range(1, 100):
        sum_errors = 0
        for i in range(0, len(test_set_prediction_input)):
            current_input = test_set_prediction_input[i]
            prediction = model.predict((numpy.asarray(current_input)).reshape(1, -1))
            if verbose:
                Support.colored_print("model output: " + str(prediction), "blue")
                Support.colored_print("real output: " + str(test_set_prediction_output[i][0]), "blue")

            error = knn.get_error_estimation(current_input, training_set_error_input, training_set_error_output, current_k)
            if verbose:
                Support.colored_print("distance based error: " + str(error), "red")
                Support.colored_print("real error: " + str(test_set_error_output[i][0]), "red")

            sum_errors += error

        avg_error = sum_errors/len(test_set_prediction_input)
        if avg_error < avg_accuracy_best_k:
            best_k = current_k
            avg_accuracy_best_k = avg_error

    Support.colored_print("Best k value: " + best_k + " with avg accuracy: " + avg_accuracy_best_k + "%", "pink")
    Support.colored_print("Completed!", "pink")