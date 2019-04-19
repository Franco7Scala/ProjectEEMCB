from __future__ import division
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.model_selection import learning_curve
from sklearn.externals import joblib
from sklearn.metrics import make_scorer
from enum import Enum
import matplotlib.pyplot as plotter
import math
import scoring
import time
import numpy
import Parser
import Support
import warnings
import sys
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class Model(Enum):
    EXTRA_TREE_REGRESSOR = 1
    GRADIENT_BOOSTING_REGRESSOR = 2
    GPML = 3


training_sets = ["/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_rf.txt", \
                 "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_rf.txt", \
                 "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_rf.txt", \
                 "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_rf.txt"]
test_sets = ["/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_rf.txt", \
             "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_rf.txt", \
             "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_rf.txt", \
             "/Users/francesco/Desktop/Cose da Sistemare/datas/ts/test_set_rf.txt"]
path_out = ["/Users/francesco/Desktop/out/rf", \
            "/Users/francesco/Desktop/out/wp", \
            "/Users/francesco/Desktop/out/wpwl", \
            "/Users/francesco/Desktop/out/wpaw"]

for current_data_set in range(0, len(training_sets)):
    path_training_set = training_sets[current_data_set]
    path_test_set = test_sets[current_data_set]
    base_path_saving = path_out[current_data_set]

    input_for_test, expected_outputs_for_test, input_size_for_test, output_size_for_test = Parser.parse_data(
        path_test_set, 0)
    output_quantity = output_size_for_test
    model_quantity = len(list(map(lambda c: c.value, Model)))

    for current_model in range(1, (model_quantity + 1)):
        selected_model = Model(current_model)

        for output_selected in range(0, output_quantity):
            # Loading sample data
            X, y, input_size, output_size = Parser.parse_data(path_training_set, 0)
            train_size = X.size
            y = y[:, output_selected]
            X_plot = numpy.zeros((1, input_size))
            X_plot[0][0] = X.item(0)

            # Fit regression model
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
                Support.colored_print("No method selected!", "red")
                sys.exit(0)
            Support.colored_print("Training " + model_name + "...", "yellow")

            t0 = time.time()
            model.fit(X[:train_size], y[:train_size])
            model_fit = time.time() - t0
            t0 = time.time()
            y_model = model.predict(X_plot)
            model_predict = time.time() - t0

            sum_relative_error_real = 0
            sum_relative_error_plus = 0
            sum_relative_error_minus = 0
            samples_quantity, _ = input_for_test.shape
            for sample_selected in range(0, samples_quantity):
                expected_output = expected_outputs_for_test[sample_selected][output_selected]
                real_output = model.predict(input_for_test[sample_selected].reshape(1, -1))
                plus_output = round(real_output)
                _, minus_output = math.modf(real_output)
                if real_output == 0:
                    real_output = 0.0001
                if plus_output == 0:
                    plus_output = 0.0001
                if minus_output == 0:
                    minus_output = 0.0001
                real_relative_error = abs((real_output - expected_output) / real_output)
                plus_relative_error = abs((plus_output - expected_output) / plus_output)
                minus_relative_error = abs((minus_output - expected_output) / minus_output)
                sum_relative_error_real += real_relative_error
                sum_relative_error_plus += plus_relative_error
                sum_relative_error_minus += minus_relative_error
            real_error = (sum_relative_error_real / samples_quantity)
            plus_error = (sum_relative_error_plus / samples_quantity)
            minus_error = (sum_relative_error_minus / samples_quantity)

            output_verbose = "Model: %s\nCurrent output: %i\nTraining time: %.3f s \nPrediction time: %.3f s\nPercentage quality real (relative error): %.2f %%\nPercentage quality plus (relative error): %.2f %%\nPercentage quality minus (relative error): %.2f %%\n" % (
            model_name, output_selected, model_fit, model_predict, real_error * 100, plus_error * 100,
            minus_error * 100)
            Support.colored_print(output_verbose, "pink")

            path_to_save = base_path_saving + "/out_" + model_name
            if not os.path.isdir(path_to_save):
                os.makedirs(path_to_save)

            path_saving_verbose_output = path_to_save + "/verbose_out_" + str(output_selected) + ".txt"
            with open(path_saving_verbose_output, "w") as text_file:
                text_file.write(output_verbose)

            # saving
            path_saving_svm_data = path_to_save + "/model_" + str(output_selected) + ".joblib"
            joblib.dump(model, path_saving_svm_data)

            # Look at the results
            Support.colored_print("Saving results...", "green")
            # train_sizes_mse, train_scores_model_mse, test_scores_model_mse = learning_curve(forest, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring="neg_mean_squared_error", cv=10)
            train_sizes_r2, train_scores_model_r2, test_scores_model_r2 = learning_curve(model, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring="r2", cv=10)
            train_sizes_re, train_scores_model_re, test_scores_model_re = learning_curve(model, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring=make_scorer( scoring.relative_error), cv=10)

            plotter.figure()
            plotter.clf()
            # plotter.plot(train_sizes_mse, -train_scores_model_mse.mean(1), 'o-', color="b", label="mean squared error")
            plotter.plot(train_sizes_r2, train_scores_model_r2.mean(1), 'o-', color="g", label="r2")
            plotter.plot(train_sizes_re, train_scores_model_re.mean(1), 'o-', color="y", label="relative error")
            plotter.xlabel("Train size")
            plotter.ylabel("Error")
            plotter.title("Learning curve for output n. " + str(output_selected) + " Training Set")
            plotter.legend(loc="best")

            path_saving_svm_image = path_to_save + "/train_model_" + str(output_selected) + ".png"
            plotter.savefig(path_saving_svm_image, dpi=400)

            plotter.clf()
            # plotter.plot(train_sizes_mse, -test_scores_model_mse.mean(1), 'o-', color="b", label="mean squared error")
            plotter.plot(train_sizes_r2, test_scores_model_r2.mean(1), 'o-', color="g", label="r2")
            plotter.plot(train_sizes_re, test_scores_model_re.mean(1), 'o-', color="y", label="relative error")
            plotter.xlabel("Train size")
            plotter.ylabel("Error")
            plotter.title("Learning curve for output n. " + str(output_selected) + " Test Set")
            plotter.legend(loc="best")

            path_saving_svm_image = path_to_save + "/test_model_" + str(output_selected) + ".png"
            plotter.savefig(path_saving_svm_image, dpi=400)


Support.colored_print("Completed!", "green")

