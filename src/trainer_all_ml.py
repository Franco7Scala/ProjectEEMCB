from __future__ import division
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor, BaggingRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, learning_curve
from sklearn.externals import joblib
from sklearn.metrics import make_scorer
from sklearn.linear_model import ElasticNetCV, LassoCV
from sklearn.cross_decomposition import PLSRegression
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
    REGRESSION_TREE = 1
    RANDOM_FOREST = 2
    EXTRA_TREE_REGRESSOR = 3
    GRADIENT_BOOSTING_REGRESSOR = 4
    BAGGING_REGRESSOR = 5
    ADABOOST_REGRESSOR = 6
    SVR = 7
    GPML = 8
    ELASTIC_NET_CV = 9
    PLS_REGRESSION = 10
    LASSO_CV = 11


path_training_set = "/home/francesco/Scrivania/datas/selector/training_set.txt"
path_test_set = "/home/francesco/Scrivania/datas/selector/test_set.txt"
base_path_saving = "/home/francesco/Scrivania"


input_for_test, expected_outputs_for_test, input_size_for_test, output_size_for_test = Parser.parse_data(path_test_set, 0)
output_quantity = output_size_for_test
model_quantity = len(list(map(lambda c: c.value, Model)))

for current_model in range(8, (model_quantity + 1)):
    selected_model = Model(current_model)

    for output_selected in range(0, output_quantity):
        # Loading sample data
        X, y, input_size, output_size = Parser.parse_data(path_training_set, 0)
        train_size = X.size
        y = y[:, output_selected]
        X_plot = numpy.zeros((1, input_size))
        X_plot[0][0] = X.item(0)

        # Fit regression model
        if selected_model == Model.SVR:
            c_param = [0.001, 0.01, 0.1, 1, 10]
            gamma_param = [0.001, 0.01, 0.1, 1]
            model = GridSearchCV(SVR(kernel='rbf'), cv=5, param_grid={"C": c_param, "gamma": gamma_param})
            model_name = "SVR"
        elif selected_model == Model.REGRESSION_TREE:
            model = DecisionTreeRegressor(criterion="mse")
            model_name = "REGRESSION_TREE"
        elif selected_model == Model.RANDOM_FOREST:
            model = RandomForestRegressor(criterion="mse", n_estimators=20, min_samples_split=4, min_weight_fraction_leaf=0.01)
            model_name = "FOREST"
        elif selected_model == Model.EXTRA_TREE_REGRESSOR:
            model = ExtraTreesRegressor(criterion="mse")
            model_name = "EXTRA_TREE_REGRESSOR"
        elif selected_model == Model.GRADIENT_BOOSTING_REGRESSOR:
            model = GradientBoostingRegressor(loss="lad", n_estimators=200)
            model_name = "GRADIENT_BOOSTING_REGRESSOR"
        elif selected_model == Model.BAGGING_REGRESSOR:
            model = BaggingRegressor(oob_score=True)
            model_name = "BAGGING_REGRESSOR"
        elif selected_model == Model.ADABOOST_REGRESSOR:
            model = AdaBoostRegressor(loss="linear")
            model_name = "ADABOOST_REGRESSOR"
        elif selected_model == Model.GPML:
            kernel = DotProduct() + WhiteKernel()
            model = GaussianProcessRegressor(kernel=kernel, random_state=0)
            model_name = "GPML"
        elif selected_model == Model.ELASTIC_NET_CV:
            model = ElasticNetCV(alphas=None, copy_X=True, cv=5, eps=0.001, fit_intercept=True,
                                 l1_ratio=0.5, max_iter=1000, n_alphas=100, n_jobs=None,
                                 normalize=False, positive=False, precompute='auto', random_state=0,
                                 selection='cyclic', tol=0.0001, verbose=0)
            model_name = "ELASTIC_NET_CV"
        elif selected_model == Model.PLS_REGRESSION:
            model = PLSRegression(n_components=2)
            model_name = "PLS_REGRESSION"
        elif selected_model == Model.LASSO_CV:
            model = LassoCV(alpha=0.1)
            model_name = "LASSO_CV"
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
        real_error = (sum_relative_error_real/samples_quantity)
        plus_error = (sum_relative_error_plus/samples_quantity)
        minus_error = (sum_relative_error_minus/samples_quantity)

        output_verbose = "Model: %s\nCurrent output: %i\nTraining time: %.3f s \nPrediction time: %.3f s\nPercentage quality real (relative error): %.2f %%\nPercentage quality plus (relative error): %.2f %%\nPercentage quality minus (relative error): %.2f %%\n" % (model_name, output_selected, model_fit, model_predict, real_error * 100, plus_error * 100, minus_error * 100)
        Support.colored_print(output_verbose, "pink")

        path_to_save = base_path_saving + "/out_" + model_name
        if not os.path.isdir(path_to_save):
            os.mkdir(path_to_save)

        path_saving_verbose_output = path_to_save + "/verbose_out_" + str(output_selected) + ".txt"
        with open(path_saving_verbose_output, "w") as text_file:
            text_file.write(output_verbose)

        # saving
        path_saving_svm_data = path_to_save + "/model_" + str(output_selected) + ".joblib"
        joblib.dump(model, path_saving_svm_data)
'''
        # Look at the results
        Support.colored_print("Saving results...", "green")
        # train_sizes_mse, train_scores_model_mse, test_scores_model_mse = learning_curve(forest, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring="neg_mean_squared_error", cv=10)
        train_sizes_r2, train_scores_model_r2, test_scores_model_r2 = learning_curve(model, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring="r2", cv=10)
        train_sizes_re, train_scores_model_re, test_scores_model_re = learning_curve(model, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring=make_scorer(scoring.relative_error), cv=10)

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
'''

Support.colored_print("Completed!", "green")

