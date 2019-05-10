import Support
import Parser
import knn
import os


if __name__ == '__main__':
    verbose = False
    k_to_try = 50
    root_directory = "/Users/francesco/Desktop/error_t/"

    for dir in os.listdir(root_directory):
        if not dir[0] == '.':
            directory_nation = root_directory + dir
            directory_nation_train = directory_nation + "/train/"
            directory_nation_test = directory_nation + "/test/"

            index_output_prediction = -1
            files = os.listdir(directory_nation_train)
            files.sort()
            for file in files:
                index_output_prediction += 1
                if not file[0] == '.':
                    path_training_set_prediction = directory_nation_train + file
                    path_test_set_prediction = directory_nation_test + file.replace("train", "test")
                    Support.colored_print("______________", "red")
                    Support.colored_print("Current file: " + path_training_set_prediction, "yellow")
                    Support.colored_print("Current file: " + path_test_set_prediction, "yellow")

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
                        sum_absolute_error = 0
                        sum_absolute_error_weighted = 0
                        for i in range(0, len(test_set_input)):
                            current_input = test_set_input[i]
                            current_output = test_set_output[i][0]
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

                            sum_absolute_error += abs(prediction - current_output)
                            sum_absolute_error_weighted += abs(prediction_weighted - current_output)

                        avg_error = sum_absolute_error / len(test_set_input)
                        avg_error_weighted = sum_absolute_error_weighted / len(test_set_input)

                        all_avg_values.append(avg_error)
                        all_avg_values_weighted.append(avg_error_weighted)

                        if avg_error < avg_accuracy_best_k:
                            best_k = current_k
                            avg_accuracy_best_k = avg_error

                        if avg_error_weighted < avg_accuracy_best_k_weighted:
                            best_k_weighted = current_k
                            avg_accuracy_best_k_weighted = avg_error_weighted

                    verbose_out = "Best k value: " + str(best_k) + " with avg accuracy (absolute error): " + str(avg_accuracy_best_k * 100) + "%\nBest k weighted value: " + str(best_k_weighted) + " with avg accuracy (absolute error): " + str(avg_accuracy_best_k_weighted * 100) + "%"
                    verbose_out += "\n\n\nValues: " + str(all_avg_values)
                    verbose_out += "\n\n\nWeighted values: " + str(all_avg_values_weighted)
                    Support.colored_print(verbose_out, "pink")

                    # save to file
                    path_to_save = directory_nation + "/output"
                    if not os.path.isdir(path_to_save):
                        os.makedirs(path_to_save)

                    path_saving_verbose_output = path_to_save + "/verbose_out_" + str(index_output_prediction) + ".txt"
                    with open(path_saving_verbose_output, "w") as text_file:
                        text_file.write(verbose_out)

    Support.colored_print("Completed!", "pink")
