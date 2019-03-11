from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

verbose = 1

#path_predictors = "/Users/francesco/Desktop/out_random_forest_regressor/forest_"
#path_test_set = "/Users/francesco/Desktop/trainingset_refixed.txt"

#path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_ADABOOST_REGRESSOR/model_"
#path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_BAGGING_REGRESSOR/model_"
#path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_ELASTIC_NET_CV/model_"
#path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_EXTRA_TREE_REGRESSOR/model_"
#path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_FOREST/model_"
#path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_GRADIENT_BOOSTING_REGRESSOR/model_"
#path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_LASSO_CV/model_"
#path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_PLS_REGRESSION/model_"
#path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_REGRESSION_TREE/model_"
#path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_SVR/model_"
path_predictors = "/Users/francesco/Desktop/out_error/out_error_5/out_GPML/model_"
path_test_set = "/Users/francesco/Desktop/Cose da Sistemare/datas/error/test_sets/test_set_other_error.txt"

input, expected_outputs, input_size, output_size = Parser.parse_data(path_test_set)
samples_quantity, _ = input.shape
output_quantity = len(expected_outputs[0])

# verifying
for output_selected in range(0, output_quantity):
    model = joblib.load(path_predictors + str(output_selected) + ".joblib")
    Support.colored_print("Verifying output n: " + str(output_selected), "blue")
    sum_relative_error = 0
    sum_absolute_error = 0
    for sample_selected in range(0, samples_quantity):
        expected_output = expected_outputs[sample_selected][output_selected]
        real_output = model.predict(input[sample_selected].reshape(1, -1))
        real_output *= 100
        if real_output == 0:
            real_output = 0.0001
        relative_error = abs((real_output - expected_output) / real_output)
        absolute_error = abs(real_output - expected_output)
        sum_relative_error += relative_error
        sum_absolute_error += absolute_error
        # showing result
        if verbose == 1:
            Support.colored_print("Sample n: " + str(sample_selected), "green")
            Support.colored_print("Expected output: " + str(expected_output), "green")
            Support.colored_print("Real output: " + str(real_output), "green")
            Support.colored_print("Relative error: " + str(relative_error), "green")
            Support.colored_print("Absolute error: " + str(relative_error), "green")
            Support.colored_print("-------------------------------------------", "green")
    # showing statistics
    Support.colored_print("-------------------------------------------", "green")
    Support.colored_print("Statistics:", "pink")
    Support.colored_print("Samples quantity: " + str(samples_quantity), "pink")
    Support.colored_print("Percentage quality (relative error): " + str(sum_relative_error / samples_quantity), "pink")
    Support.colored_print("Percentage quality (absolute error): " + str(sum_absolute_error / samples_quantity), "pink")

Support.colored_print("Done!", "red")