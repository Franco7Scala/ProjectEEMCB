from __future__ import division
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.externals import joblib
import time
import sys
import os
import knn
import Nation
import Model
import parser
import support
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


if len(sys.argv) == 1 or sys.argv[1] == "help":
    support.colored_print("Usage:\n\t-parameter 1: nation code\n\t-parameter 2: source id (int)\n\t-parameter 3: verbose (bool)", "red")
    sys.exit(0)

nation_code = sys.argv[1]
source_id = int(sys.argv[2])
verbose = bool(sys.argv[3])

nation = Nation.load_nation(nation_code)

selected_model = Model.Model(nation.sources[source_id].best_model)
training_set_input, training_set_output, _, _ = parser.parse_data(nation.base_path_datas + nation.sources[source_id].path_training_set_prediction)
test_size = 200
train_size = len(training_set_input) - test_size
training_set_output = training_set_output[:, source_id]

# setup
if selected_model == Model.Model.EXTRA_TREE_REGRESSOR:
    model = ExtraTreesRegressor(criterion="mse")
    model_name = "EXTRA_TREE_REGRESSOR"
elif selected_model == Model.Model.GRADIENT_BOOSTING_REGRESSOR:
    model = GradientBoostingRegressor(loss="lad", n_estimators=200)
    model_name = "GRADIENT_BOOSTING_REGRESSOR"
elif selected_model == Model.Model.GPML:
    kernel = DotProduct() + WhiteKernel()
    model = GaussianProcessRegressor(kernel=kernel, random_state=0)
    model_name = "GPML"
else:
    support.colored_print("No method selected!", "red")
    sys.exit(0)

if verbose:
    support.colored_print("Training...", "green")

# training
t0 = time.time()
model.fit(training_set_input[:train_size], training_set_output[:train_size])
model_fit_time = time.time() - t0

# testing
sum_relative_error = 0

for sample_selected in range(train_size, (train_size + test_size)):
    expected_output = training_set_output[sample_selected]
    output = model.predict(training_set_input[sample_selected].reshape(1, -1))
    if output == 0:
        output = 0.0001

    relative_error = abs((output - expected_output) / output)
    sum_relative_error += relative_error

error = (sum_relative_error / test_size)

# showing statistics
verbose_out_prediction = "Output n: %i\nModel: %s\nTraining time: %.3f s \nPercentage quality (relative error): %.2f %%" % (source_id, model_name, model_fit_time, error * 100)
if verbose:
    support.colored_print(verbose_out_prediction, "blue")

if verbose:
    support.colored_print("Saving model...", "green")

# making saving directory
if not os.path.isdir(nation.base_path_datas):
    os.makedirs(nation.base_path_datas)

# saving model
joblib.dump(model, nation.base_path_datas + nation.sources[source_id].path_model)

# generating training set error
if verbose:
    support.colored_print("Generating training set error...", "green")

file_training_set_error = open(nation.base_path_datas + nation.sources[source_id].path_training_set_error, "w+")

for sample_selected in range(0, train_size):
    expected_output = training_set_output[sample_selected]
    real_output = model.predict(training_set_input[sample_selected].reshape(1, -1))
    relative_error = support.calculate_relative_error(real_output, expected_output)
    for current_input in range(0, len(training_set_input[sample_selected])):
        file_training_set_error.write("%f " % training_set_input[sample_selected][current_input])

    file_training_set_error.write("= %lf\n" % (relative_error * 100))

file_training_set_error.close()

# calculating quality error estimator
if verbose:
    support.colored_print("Calculating quality error estimator...", "green")

set_input_error, set_output_error, _, _ = parser.parse_data(nation.base_path_datas + nation.sources[source_id].path_training_set_error)
test_set_input_error = set_input_error[-test_size:]
test_set_output_error = set_output_error[-test_size:]
sum_absolute_error = 0
for i in range(0, len(test_set_input_error)):
    current_input = test_set_input_error[i]
    current_output = test_set_output_error[i]
    prediction = knn.get_error_estimation(current_input, set_input_error[:-test_size], set_output_error[:-test_size], nation.sources[source_id].best_k, nation.sources[source_id].k_weighted)
    sum_absolute_error += abs(prediction - current_output)

avg_error = sum_absolute_error / len(test_set_input_error)
verbose_out_error = "Best k value for error estimation: " + str(nation.sources[source_id].best_k) + "\nAvg accuracy error estimator (absolute error): %.2f" % avg_error
if verbose:
    support.colored_print(verbose_out_error, "blue")

if verbose:
    support.colored_print("Saving statistics...", "green")

with open(nation.base_path_datas + nation.sources[source_id].path_statistics_training, "w") as text_file:
    text_file.write(verbose_out_prediction + "\n" + verbose_out_error)

support.colored_print("Completed!", "pink")
