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


nation_id = sys.argv[1]
source_id = int(sys.argv[2])
verbose = bool(sys.argv[3])

nation = Nation.load_nation(nation_id)


selected_model = Model(nation.sources[source_id].best_model)
training_set_input, training_set_output, input_size, output_size = parser.parse_data(nation.path_training_set_prediction, 0)
test_size = 200
train_size = training_set_input.size - test_size
training_set_output = training_set_output[:, source_id]

# setup
if selected_model == Model.EXTRA_TREE_REGRESSOR:
    model = ExtraTreesRegressor(criterion="mse")
    model_name = "EXTRA_TREE_REGRESSOR"
elif selected_model == Model.GRADIENT_BOOSTING_REGRESSOR:
    model = GradientBoostingRegressor(loss="lad", n_estimators=200)
    model_name = "GRADIENT_BOOSTING_REGRESSOR"
elif selected_model == Model.GPML:
    kernel = DotProduct() + WhiteKernel()
    model = GaussianProcessRegressor(kernel=kernel, random_state=0)
    model_name = "GPML"
else:
    support.colored_print("No method selected!", "red")
    sys.exit(0)

support.colored_print("Training " + model_name + "...", "yellow")

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
output_verbose = "Model: %s\nCurrent output: %i\nTraining time: %.3f s \nPercentage quality real (relative error): %.2f %%\n" % (model_name, source_id, model_fit_time, error * 100)
support.colored_print(output_verbose, "green")

# saving statistics
path_to_save = nation.path_datas
if not os.path.isdir(path_to_save):
    os.makedirs(path_to_save)

with open(nation.sources[source_id].path_statistics_training, "w") as text_file:
    text_file.write(output_verbose)

# saving model
joblib.dump(model, nation.sources[source_id].path_model)

# generating training set error
test_set_input = training_set_input[-200:]
test_set_output = training_set_output[-200:, source_id]
sum_absolute_error = 0
for i in range(0, len(test_set_input)):
    current_input = test_set_input[i]
    current_output = test_set_output[i][0]
    prediction = knn.get_error_estimation(current_input, training_set_input, training_set_output, nation.sources[source_id].best_k, False)
    if verbose:
        support.colored_print("Real output: " + str(current_output), "blue")

    if prediction == 0:
        prediction = 0.0001

    sum_absolute_error += abs(prediction - current_output)

avg_error = sum_absolute_error / len(test_set_input)
verbose_out = "Best k value: " + str(nation.sources[source_id].best_k) + " with avg accuracy (absolute error): " + str(avg_error) + "%\n"
if verbose:
    support.colored_print(verbose_out, "green")

with open(nation.sources[source_id].path_statistics_error, "w") as text_file:
    text_file.write(verbose_out)

support.colored_print("Completed!", "pink")