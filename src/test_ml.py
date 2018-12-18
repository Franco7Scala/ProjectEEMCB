from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


#path_predictors = "/Users/francesco/Desktop/out_random_forest_regressor/forest_"
#path_test_set = "/Users/francesco/Desktop/trainingset_refixed.txt"

path_predictors = "/Users/francesco/Desktop/out_EXTRA_TREE_REGRESSOR_wpaw/model_"
path_test_set = "/Users/francesco/Desktop/test_set_wpaw.txt"

input, expected_outputs, input_size, output_size = Parser.parse_data(path_test_set)
samples_quantity,_ = input.shape
output_quantity = len(expected_outputs[0])

# verifying
for output_selected in range(0, output_quantity):
    model = joblib.load(path_predictors + str(output_selected) + ".joblib")
    Support.colored_print("Verifying output n: " + str(output_selected), "blue")
    sum_relative_error = 0
    for sample_selected in range(0, samples_quantity):
        expected_output = expected_outputs[sample_selected][output_selected]
        real_output = model.predict(input[sample_selected].reshape(1, -1))
        relative_error = abs((real_output - expected_output) / real_output)
        sum_relative_error += relative_error
        # showing result
        #Support.colored_print("Sample n: " + str(sample_selected), "green")
        #Support.colored_print("Expected output: " + str(expected_output), "green")
        #Support.colored_print("Real output: " + str(real_output), "green")
        #Support.colored_print("Relative error: " + str(relative_error), "green")
        #Support.colored_print("-------------------------------------------", "green")
    # showing statistics
    Support.colored_print("-------------------------------------------", "green")
    Support.colored_print("Statistics:", "pink")
    Support.colored_print("Samples quantity: " + str(samples_quantity), "pink")
    Support.colored_print("Percentage quality (relative error): " + str(sum_relative_error/samples_quantity), "pink")

Support.colored_print("Done!", "red")