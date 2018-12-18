from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


#path_predictors = "/Users/francesco/Desktop/out_random_forest_regressor/forest_"
#path_test_set = "/Users/francesco/Desktop/trainingset_refixed.txt"

path_predictors = "/Users/francesco/Desktop/out_random_forest_wpaw_v2/forest_"
path_test_set = "/Users/francesco/Desktop/test_set_wpaw.txt"


input, expected_outputs, input_size, output_size = Parser.parse_data(path_test_set)
samples_quantity,_ = input.shape
output_quantity = len(expected_outputs[0])

# verifying
model = joblib.load(path_predictors + "3.joblib")
sum_relative_error_model = 0
sum_relative_error_retrieved = 0
for sample_selected in range(0, samples_quantity):
    calculated_value = input[sample_selected][3] + \
                       input[sample_selected][4] + \
                       input[sample_selected][5] + \
                       input[sample_selected][6] - \
                       input[sample_selected][7] + \
                       input[sample_selected][8]
    for output_selected in range(0, output_quantity):
        if output_selected != 3:
            calculated_value += expected_outputs[sample_selected][output_selected]

    expected_output = expected_outputs[sample_selected][3]
    real_output = model.predict(input[sample_selected].reshape(1, -1))
    retrieved_output = calculated_value

    Support.colored_print("-------------------------------------------", "blue")
    Support.colored_print("expected: " + str(expected_output), "green")
    Support.colored_print("model: " + str(real_output), "green")
    Support.colored_print("retrieved: " + str(retrieved_output), "green")

    relative_error_model = abs((real_output - expected_output) / real_output)
    relative_error_retrieved = abs((retrieved_output - expected_output) / retrieved_output)
    sum_relative_error_model += relative_error_model
    sum_relative_error_retrieved += relative_error_retrieved

# showing statistics
Support.colored_print("Statistics:", "pink")
Support.colored_print("Samples quantity: " + str(samples_quantity), "pink")
Support.colored_print("Percentage quality (relative error) model: " + str(sum_relative_error_model/samples_quantity), "pink")
Support.colored_print("Percentage quality (relative error) retrieved: " + str(sum_relative_error_retrieved/samples_quantity), "pink")

Support.colored_print("Done!", "red")