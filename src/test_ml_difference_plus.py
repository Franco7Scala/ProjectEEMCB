from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)

detailed_verbose = 1

path_predictor_fossil_coal = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_coal.joblib"            # wp
path_predictor_fossil_gas = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_gas.joblib"              # wpwl
path_predictor_hard_coal = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/hard_coal.joblib"                # wpwl
path_predictor_fossil_oil = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_oil.joblib"              # ---------------------------------------- wpwl
path_predictor_waste = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/waste.joblib"                        # wpwl
path_predictor_other = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/other.joblib"                        # wpaw
path_predictor_dispersion = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/dispersion.joblib"              # wpwl_s

path_data_wp = "/Users/francesco/Desktop/Cose da Sistemare/ts/test_set_wp.txt"
path_data_wpwl = "/Users/francesco/Desktop/Cose da Sistemare/ts/test_set_wpwl.txt"
path_data_wpaw = "/Users/francesco/Desktop/Cose da Sistemare/ts/test_set_wpaw.txt"
path_data_wpwl_s = "/Users/francesco/Desktop/Cose da Sistemare/ts/test_set_wpwl_s.txt"


input_wp, expected_outputs_wp, input_size_wp, output_size_wp = Parser.parse_data(path_data_wp, 0)
input_wpwl, expected_outputs_wpwl, input_size_wpwl, output_size_wpwl = Parser.parse_data(path_data_wpwl, 0)
input_wpaw, expected_outputs_wpaw, input_size_wpaw, output_size_wpaw = Parser.parse_data(path_data_wpaw, 0)
input_wpwl_s, expected_outputs_wpwl_s, input_size_wpwl_s, output_size_wpwl_s = Parser.parse_data(path_data_wpwl_s, 0)


samples_quantity,_ = input_wp.shape
output_quantity_wp = len(expected_outputs_wp[0])
output_quantity_wpwl = len(expected_outputs_wpwl[0])
output_quantity_wpwl_s = len(expected_outputs_wpwl_s[0])

model_fossil_coal = joblib.load(path_predictor_fossil_coal)
model_fossil_gas = joblib.load(path_predictor_fossil_gas)
model_hard_coal = joblib.load(path_predictor_hard_coal)
model_waste = joblib.load(path_predictor_waste)
model_other = joblib.load(path_predictor_other)
model_dispersion = joblib.load(path_predictor_dispersion)
model_fossil_oil = joblib.load(path_predictor_fossil_oil)

# verifying
sum_relative_error_model = 0
sum_relative_error_retrieved = 0
for sample_selected in range(0, samples_quantity):
    production = model_fossil_coal.predict(input_wp[sample_selected].reshape(1, -1)) + \
                 model_fossil_gas.predict(input_wpwl[sample_selected].reshape(1, -1)) + \
                 model_hard_coal.predict(input_wpwl[sample_selected].reshape(1, -1)) + \
                 model_waste.predict(input_wpwl[sample_selected].reshape(1, -1)) + \
                 model_other.predict(input_wpaw[sample_selected].reshape(1, -1)) + \
                 model_dispersion.predict(input_wpwl_s[sample_selected].reshape(1, -1)) + \
                 input_wp[sample_selected][3] + \
                 input_wp[sample_selected][4] + \
                 input_wp[sample_selected][5] + \
                 input_wp[sample_selected][6] - \
                 input_wp[sample_selected][8]       # transits

    expected_output = expected_outputs_wp[sample_selected][3]
    real_output = model_fossil_oil.predict(input_wpwl[sample_selected].reshape(1, -1))
    retrieved_output = input_wp[sample_selected][7] - production

    if detailed_verbose != 0:
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