from __future__ import division
from sklearn.externals import joblib
from enum import Enum
import Parser
import Support
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)


class Model(Enum):
    REGRESSION_TREE = 1
    RANDOM_FOREST = 2
    EXTRA_TREE_REGRESSOR = 3
    GRADIENT_BOOSTING_REGRESSOR = 4
    BAGGING_REGRESSOR = 5
    ADABOOST_REGRESSOR = 6
    SVR = 7


detailed_verbose = 0
position_output = 3
training = 0


path_selector = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/selector_test.joblib"
path_predictor_SVR = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/fossil_oil/SVR.joblib"
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

model_selector = joblib.load(path_selector)
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

    selector_output = model_selector.predict(input_rf[sample_selected].reshape(1, -1))
    #TODO select type ceil!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    current_model = 4
    selected_output = Model(current_model)

    real_output = 0.0001
    if selected_output == Model.SVR:
        real_output = model_SVR.predict(input_rf[sample_selected].reshape(1, -1))
    elif selected_output == Model.REGRESSION_TREE:
        real_output = model_RegressionTree.predict(input_rf[sample_selected].reshape(1, -1))
    elif selected_output == Model.RANDOM_FOREST:
        real_output = model_RandomForest.predict(input_wpaw[sample_selected].reshape(1, -1))
    elif selected_output == Model.EXTRA_TREE_REGRESSOR:
        real_output = model_ExtraTreeRegressor.predict(input_wp[sample_selected].reshape(1, -1))
    elif selected_output == Model.GRADIENT_BOOSTING_REGRESSOR:
        real_output = model_GBRT.predict(input_wpwl[sample_selected].reshape(1, -1))
    elif selected_output == Model.BAGGING_REGRESSOR:
        real_output = model_BaggingRegressor.predict(input_wpaw[sample_selected].reshape(1, -1))
    elif selected_output == Model.ADABOOST_REGRESSOR:
        real_output = model_AdaBoostRegressor.predict(input_rf[sample_selected].reshape(1, -1))

    if detailed_verbose != 0:
        Support.colored_print("-------------------------------------------", "blue")
        Support.colored_print("expected: " + str(expected_output), "green")
        Support.colored_print("model selected: " + str(selected_output), "green")
        Support.colored_print("model output: " + str(real_output), "green")

    if real_output == 0:
        real_output = 0.0001
    relative_error = abs((real_output - expected_output) / (real_output))
    sum_relative_error_model += relative_error

# showing statistics
Support.colored_print("Statistics:", "pink")
Support.colored_print("Samples quantity: " + str(samples_quantity), "pink")
Support.colored_print("Percentage quality (relative error) model: " + str(sum_relative_error_model/samples_quantity), "pink")

Support.colored_print("Done!", "red")