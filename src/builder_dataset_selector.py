from __future__ import division
from sklearn.externals import joblib
import Parser
import Support
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)

detailed_verbose = 0
position_output = 3
training = 0
path_output = "/Users/francesco/Desktop/output.txt"

f = open(path_output, "w+")

path_predictor_SVR = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_oil/SVM.joblib"
#path_predictor_KRR = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_oil/KRR.joblib"
path_predictor_RegressionTree = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_oil/RegressionTree.joblib"
path_predictor_RandomForest = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_oil/RandomForest.joblib"
path_predictor_GBRT = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_oil/GBRT.joblib"
path_predictor_BaggingRegressor = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_oil/BaggingRegressor.joblib"
path_predictor_ExtraTreeRegressor = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_oil/ExtraTree.joblib"
path_predictor_AdaBoostRegressor = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_oil/AdaBoost.joblib"

if training == 0:
    path_data_rf = "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_rf.txt"
    path_data_wp = "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_wp.txt"
    path_data_wpwl = "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_wpwl.txt"
    path_data_wpaw = "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_wpaw.txt"
else:
    path_data_rf = "/Users/francesco/Desktop/Cose da Sistemare/datas/ds/training_set_rf.txt"
    path_data_wp = "/Users/francesco/Desktop/Cose da Sistemare/datas/ds/training_set_wp.txt"
    path_data_wpwl = "/Users/francesco/Desktop/Cose da Sistemare/datas/ds/training_set_wpwl.txt"
    path_data_wpaw = "/Users/francesco/Desktop/Cose da Sistemare/datas/ds/training_set_wpaw.txt"


input_rf, expected_outputs_rf, input_size_rf, output_size_rf = Parser.parse_data(path_data_rf, 0)
input_wp, expected_outputs_wp, input_size_wp, output_size_wp = Parser.parse_data(path_data_wp, 0)
input_wpwl, expected_outputs_wpwl, input_size_wpwl, output_size_wpwl = Parser.parse_data(path_data_wpwl, 0)
input_wpaw, expected_outputs_wpaw, input_size_wpaw, output_size_wpaw = Parser.parse_data(path_data_wpaw, 0)

samples_quantity,_ = input_wp.shape

output_quantity_rf = len(expected_outputs_rf[0])
output_quantity_wp = len(expected_outputs_wp[0])
output_quantity_wpwl = len(expected_outputs_wpwl[0])
output_quantity_wpaw = len(expected_outputs_wpaw[0])

model_SVR = joblib.load(path_predictor_SVR)
#model_KRR = joblib.load(path_predictor_KRR)
model_RegressionTree = joblib.load(path_predictor_RegressionTree)
model_RandomForest = joblib.load(path_predictor_RandomForest)
model_GBRT = joblib.load(path_predictor_GBRT)
model_BaggingRegressor = joblib.load(path_predictor_BaggingRegressor)
model_ExtraTreeRegressor = joblib.load(path_predictor_ExtraTreeRegressor)
model_AdaBoostRegressor = joblib.load(path_predictor_AdaBoostRegressor)


# verifying
sum_relative_error_model = 0
for sample_selected in range(0, samples_quantity):
    expected_output = expected_outputs_wp[sample_selected][position_output]

    real_output_SVR = model_SVR.predict(input_rf[sample_selected].reshape(1, -1))
    #real_output_KRR = model_KRR.predict(input_wp[sample_selected].reshape(1, -1))
    real_output_RegressionTree = model_RegressionTree.predict(input_rf[sample_selected].reshape(1, -1))
    real_output_RandomForest = model_RandomForest.predict(input_wpaw[sample_selected].reshape(1, -1))
    real_output_GBRT = model_GBRT.predict(input_wpwl[sample_selected].reshape(1, -1))
    real_output_BaggingRegressor = model_BaggingRegressor.predict(input_wpaw[sample_selected].reshape(1, -1))
    real_output_ExtraTreeRegressor = model_ExtraTreeRegressor.predict(input_wp[sample_selected].reshape(1, -1))
    real_output_AdaBoostRegressor = model_AdaBoostRegressor.predict(input_rf[sample_selected].reshape(1, -1))

    if detailed_verbose != 0:
        Support.colored_print("-------------------------------------------", "blue")
        Support.colored_print("expected: " + str(expected_output), "green")
        Support.colored_print("model SVR: " + str(real_output_SVR), "green")
        #Support.colored_print("model KRR: " + str(real_output_KRR), "green")
        Support.colored_print("model RegressionTree: " + str(real_output_RegressionTree), "green")
        Support.colored_print("model RandomForest: " + str(real_output_RandomForest), "green")
        Support.colored_print("model GBRT: " + str(real_output_GBRT), "green")
        Support.colored_print("model BaggingRegressor: " + str(real_output_BaggingRegressor), "green")
        Support.colored_print("model ExtraTreeRegressor: " + str(real_output_ExtraTreeRegressor), "green")
        Support.colored_print("model AdaBoostRegressor: " + str(real_output_AdaBoostRegressor), "green")

    errors = [0, 0, 0, 0, 0, 0, 0]

    # relative_error_model_KRR = abs((real_output_KRR - expected_output) / real_output_KRR)

    if real_output_SVR != 0:
        relative_error_model_SVR = abs((real_output_SVR - expected_output) / real_output_SVR)
    else:
        relative_error_model_SVR = abs((real_output_SVR - expected_output) / (real_output_SVR + 0.0001))

    if real_output_RegressionTree != 0:
        relative_error_model_RegressionTree = abs((real_output_RegressionTree - expected_output) / real_output_RegressionTree)
    else:
        relative_error_model_RegressionTree = abs((real_output_RegressionTree - expected_output) / (real_output_RegressionTree + 0.0001))

    if real_output_RandomForest != 0:
        relative_error_model_RandomForest = abs((real_output_RandomForest - expected_output) / real_output_RandomForest)
    else:
        relative_error_model_RandomForest = abs((real_output_RandomForest - expected_output) / (real_output_RandomForest + 0.0001))

    if real_output_GBRT != 0:
        relative_error_model_GBRT = abs((real_output_GBRT - expected_output) / real_output_GBRT)
    else:
        relative_error_model_GBRT = abs((real_output_GBRT - expected_output) / (real_output_GBRT + 0.0001))

    if real_output_BaggingRegressor != 0:
        relative_error_model_BaggingRegressor = abs((real_output_BaggingRegressor - expected_output) / real_output_BaggingRegressor)
    else:
        relative_error_model_BaggingRegressor = abs((real_output_BaggingRegressor - expected_output) / (real_output_BaggingRegressor + 0.0001))

    if real_output_ExtraTreeRegressor != 0:
        relative_error_model_ExtraTreeRegressor = abs((real_output_ExtraTreeRegressor - expected_output) / real_output_ExtraTreeRegressor)
    else:
        relative_error_model_ExtraTreeRegressor = abs((real_output_ExtraTreeRegressor - expected_output) / (real_output_ExtraTreeRegressor + 0.0001))

    if real_output_AdaBoostRegressor != 0:
        relative_error_model_AdaBoostRegressor = abs((real_output_AdaBoostRegressor - expected_output) / real_output_AdaBoostRegressor)
    else:
        relative_error_model_AdaBoostRegressor = abs((real_output_AdaBoostRegressor - expected_output) / (real_output_AdaBoostRegressor + 0.0001))


    errors[0] = relative_error_model_SVR
    #errors[1] = relative_error_model_KRR
    errors[1] = relative_error_model_RegressionTree
    errors[2] = relative_error_model_RandomForest
    errors[3] = relative_error_model_GBRT
    errors[4] = relative_error_model_BaggingRegressor
    errors[5] = relative_error_model_ExtraTreeRegressor
    errors[6] = relative_error_model_AdaBoostRegressor

    best_model_index = 0
    min_error = errors[best_model_index]
    for i in range(1, len(errors)):
        if min_error > errors[i]:
            min_error = errors[i]
            best_model_index = i

    sum_relative_error_model += min_error

    for current_input in range(0, len(input_rf[sample_selected])):
        f.write("%f " % input_rf[sample_selected][current_input])
    f.write("= %d" % best_model_index)
    f.write("\n")

f.close()
# showing statistics
Support.colored_print("Statistics:", "pink")
Support.colored_print("Samples quantity: " + str(samples_quantity), "pink")
Support.colored_print("Percentage quality (relative error) model (maximum reachable): " + str(sum_relative_error_model/samples_quantity), "pink")

Support.colored_print("Done!", "red")