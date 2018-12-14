from __future__ import division
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import learning_curve
from sklearn.externals import joblib
from sklearn.metrics import make_scorer
import matplotlib.pyplot as plotter
import src.scoring
import time
import numpy
import src.Parser
import src.Support
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


output_quantity = 6
path_training_set = "/Users/francesco/Desktop/test_set_1.txt"
base_path_saving = "/Users/francesco/Desktop"

for output_selected in range(0, output_quantity):
    # Loading sample data
    src.Support.colored_print("Loading training set...", "green")
    X, y, input_size, output_size = src.Parser.parse_data(path_training_set)
    train_size = X.size
    y = y[:, output_selected]
    X_plot = numpy.zeros((1, input_size))
    X_plot[0][0] = X.item(0)

    # Fit regression model
    src.Support.colored_print("Training...", "green")
    kr = GridSearchCV(KernelRidge(kernel='rbf', gamma=0.1), cv=5, param_grid={"alpha": [1e0, 0.1, 1e-2, 1e-3], "gamma": numpy.logspace(-2, 2, 5)})
    t0 = time.time()
    kr.fit(X[:train_size], y[:train_size])
    kr_fit = time.time() - t0
    print("KRR complexity and bandwidth selected and model fitted in %.3f s" % kr_fit)
    t0 = time.time()
    y_kr = kr.predict(X_plot)
    kr_predict = time.time() - t0
    print("KRR prediction for %d inputs in %.3f s" % (X_plot.shape[0], kr_predict))

    # Look at the results
    src.Support.colored_print("Showing results...", "green")
    kr_result = KernelRidge(kernel='rbf', alpha=0.1, gamma=0.1)
    train_sizes_mse, train_scores_svr_mse, test_scores_svr_mse = learning_curve(kr_result, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring="neg_mean_squared_error", cv=10)
    train_sizes_r2, train_scores_svr_r2, test_scores_svr_r2 = learning_curve(kr_result, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring="r2", cv=10)
    train_sizes_re, train_scores_svr_re, test_scores_svr_re = learning_curve(kr_result, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring=make_scorer(
        src.scoring.relative_error), cv=10)

    plotter.figure()
    plotter.clf()
    #plotter.plot(train_sizes_mse, -train_scores_svr_mse.mean(1), 'o-', color="b", label="mean squared error")
    plotter.plot(train_sizes_r2, train_scores_svr_r2.mean(1), 'o-', color="g", label="r2")
    plotter.plot(train_sizes_re, train_scores_svr_re.mean(1), 'o-', color="y", label="relative error")
    plotter.xlabel("Train size")
    plotter.ylabel("Error")
    plotter.title("Learning curve for output n. " + str(output_selected) + " Training Set")
    plotter.legend(loc="best")

    path_saving_svm_image = base_path_saving + "/train_svm_" + str(output_selected) + ".png"
    plotter.savefig(path_saving_svm_image, dpi=400)

    plotter.clf()
    #plotter.plot(train_sizes_mse, -test_scores_svr_mse.mean(1), 'o-', color="b", label="mean squared error")
    plotter.plot(train_sizes_r2, test_scores_svr_r2.mean(1), 'o-', color="g", label="r2")
    plotter.plot(train_sizes_re, test_scores_svr_re.mean(1), 'o-', color="y", label="relative error")
    plotter.xlabel("Train size")
    plotter.ylabel("Error")
    plotter.title("Learning curve for output n. " + str(output_selected) + " Test Set")
    plotter.legend(loc="best")

    path_saving_svm_image = base_path_saving + "/test_krr_" + str(output_selected) + ".png"
    plotter.savefig(path_saving_svm_image, dpi=400)

    # saving
    path_saving_svm_data = base_path_saving + "/krr_" + str(output_selected) + ".joblib"
    joblib.dump(kr, path_saving_svm_data)

src.Support.colored_print("Completed!", "pink")
