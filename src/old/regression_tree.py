from __future__ import division
from sklearn.tree import DecisionTreeRegressor
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
    tree = DecisionTreeRegressor(criterion="mse")
    t0 = time.time()
    tree.fit(X[:train_size], y[:train_size])
    tree_fit = time.time() - t0
    print("TREE complexity and bandwidth selected and model fitted in %.3f s" % tree_fit)
    t0 = time.time()
    y_tree = tree.predict(X_plot)
    tree_predict = time.time() - t0
    print("TREE prediction for %d inputs in %.3f s" % (X_plot.shape[0], tree_predict))

    # Look at the results
    src.Support.colored_print("Saving results...", "green")
    tree_results = tree
    #train_sizes_mse, train_scores_tree_mse, test_scores_tree_mse = learning_curve(tree_results, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring="neg_mean_squared_error", cv=10)
    train_sizes_r2, train_scores_tree_r2, test_scores_tree_r2 = learning_curve(tree_results, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring="r2", cv=10)
    train_sizes_re, train_scores_tree_re, test_scores_tree_re = learning_curve(tree_results, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring=make_scorer(
        src.scoring.relative_error), cv=10)

    plotter.figure()
    plotter.clf()
    #plotter.plot(train_sizes_mse, -train_scores_tree_mse.mean(1), 'o-', color="b", label="mean squared error")
    plotter.plot(train_sizes_r2, train_scores_tree_r2.mean(1), 'o-', color="g", label="r2")
    plotter.plot(train_sizes_re, train_scores_tree_re.mean(1), 'o-', color="y", label="relative error")
    plotter.xlabel("Train size")
    plotter.ylabel("Error")
    plotter.title("Learning curve for output n. " + str(output_selected) + " Training Set")
    plotter.legend(loc="best")

    path_saving_svm_image = base_path_saving + "/train_svm_" + str(output_selected) + ".png"
    plotter.savefig(path_saving_svm_image, dpi=400)

    plotter.clf()
    #plotter.plot(train_sizes_mse, -test_scores_tree_mse.mean(1), 'o-', color="b", label="mean squared error")
    plotter.plot(train_sizes_r2, test_scores_tree_r2.mean(1), 'o-', color="g", label="r2")
    plotter.plot(train_sizes_re, test_scores_tree_re.mean(1), 'o-', color="y", label="relative error")
    plotter.xlabel("Train size")
    plotter.ylabel("Error")
    plotter.title("Learning curve for output n. " + str(output_selected) + " Test Set")
    plotter.legend(loc="best")

    path_saving_svm_image = base_path_saving + "/test_tree_" + str(output_selected) + ".png"
    plotter.savefig(path_saving_svm_image, dpi=400)

    # saving
    path_saving_svm_data = base_path_saving + "/tree_" + str(output_selected) + ".joblib"
    joblib.dump(tree, path_saving_svm_data)

src.Support.colored_print("Completed!", "pink")

