from __future__ import division
import time
import numpy
import Parser
import Support
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import learning_curve
from sklearn.kernel_ridge import KernelRidge
from sklearn.externals import joblib
import matplotlib.pyplot as plotter


output_selected = 0
path_training_set = "/Users/francesco/Desktop/test_set_1.txt"
path_saving_svm = "/Users/francesco/Desktop/svm_" + str(output_selected) + ".joblib"
path_saving_kr = "/Users/francesco/Desktop/kr_" + str(output_selected) + ".joblib"
# #############################################################################
# Loading sample data
Support.colored_print("Loading training set...", "green")
X, y, input_size, output_size = Parser.parse_data(path_training_set)
train_size = X.size
y = y[:, output_selected]

X_plot = numpy.zeros((1, input_size))
X_plot[0][0] = X.item(0)
# #############################################################################
# Fit regression model
Support.colored_print("Training...", "green")
svr = GridSearchCV(SVR(kernel='rbf', gamma=0.1), cv=5, param_grid={"C": [1e0, 1e1, 1e2, 1e3], "gamma": numpy.logspace(-2, 2, 5)})
kr = GridSearchCV(KernelRidge(kernel='rbf', gamma=0.1), cv=5, param_grid={"alpha": [1e0, 0.1, 1e-2, 1e-3], "gamma": numpy.logspace(-2, 2, 5)})

t0 = time.time()
svr.fit(X[:train_size], y[:train_size])
svr_fit = time.time() - t0
print("SVR complexity and bandwidth selected and model fitted in %.3f s" % svr_fit)

t0 = time.time()
kr.fit(X[:train_size], y[:train_size])
kr_fit = time.time() - t0
print("KRR complexity and bandwidth selected and model fitted in %.3f s" % kr_fit)

sv_ratio = svr.best_estimator_.support_.shape[0] / train_size
print("Support vector ratio: %.3f" % sv_ratio)

t0 = time.time()
y_svr = svr.predict(X_plot)
svr_predict = time.time() - t0
print("SVR prediction for %d inputs in %.3f s" % (X_plot.shape[0], svr_predict))

t0 = time.time()
y_kr = kr.predict(X_plot)
kr_predict = time.time() - t0
print("KRR prediction for %d inputs in %.3f s" % (X_plot.shape[0], kr_predict))

# #############################################################################
# Look at the results
Support.colored_print("Showing results...", "green")
sv_ind = svr.best_estimator_.support_

#plotter.scatter(X[sv_ind], y[sv_ind], c='r', s=50, label='SVR support vectors', zorder=2, edgecolors=(0, 0, 0))
#plotter.scatter(X[:train_size], y[:train_size], c='k', label='data', zorder=1, edgecolors=(0, 0, 0))
plotter.plot(X_plot, y_svr, c='r', label='SVR (fit: %.3fs, predict: %.3fs)' % (svr_fit, svr_predict))
plotter.plot(X_plot, y_kr, c='g', label='KRR (fit: %.3fs, predict: %.3fs)' % (kr_fit, kr_predict))
plotter.xlabel('data')
plotter.ylabel('target')
plotter.title('SVR versus Kernel Ridge')
plotter.legend()

# Visualize training and prediction time
plotter.figure()

# Generate sample data
sizes = numpy.logspace(1, 4, 7).astype(numpy.int)
for name, estimator in {"KRR": KernelRidge(kernel='rbf', alpha=0.1, gamma=10),
                        "SVR": SVR(kernel='rbf', C=1e1, gamma=10)}.items():
    train_time = []
    test_time = []
    for train_test_size in sizes:
        t0 = time.time()
        estimator.fit(X[:train_test_size], y[:train_test_size])
        train_time.append(time.time() - t0)

        t0 = time.time()
        estimator.predict(X_plot[:1000])
        test_time.append(time.time() - t0)

    plotter.plot(sizes, train_time, 'o-', color="r" if name == "SVR" else "g", label="%s (train)" % name)
    plotter.plot(sizes, test_time, 'o--', color="r" if name == "SVR" else "g", label="%s (test)" % name)

plotter.xscale("log")
plotter.yscale("log")
plotter.xlabel("Train size")
plotter.ylabel("Time (seconds)")
plotter.title('Execution Time')
plotter.legend(loc="best")

# Visualize learning curves
plotter.figure()

svr = SVR(kernel='rbf', C=1e1, gamma=0.1)
kr = KernelRidge(kernel='rbf', alpha=0.1, gamma=0.1)
train_sizes, train_scores_svr, test_scores_svr = learning_curve(svr, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring="neg_mean_squared_error", cv=10)
train_sizes_abs, train_scores_kr, test_scores_kr = learning_curve(kr, X[:train_size], y[:train_size], train_sizes=numpy.linspace(0.1, 1, 10), scoring="neg_mean_squared_error", cv=10)

plotter.plot(train_sizes, -test_scores_svr.mean(1), 'o-', color="r", label="SVR")
plotter.plot(train_sizes, -test_scores_kr.mean(1), 'o-', color="g", label="KRR")
plotter.xlabel("Train size")
plotter.ylabel("Mean Squared Error")
plotter.title('Learning curves')
plotter.legend(loc="best")
plotter.show()

joblib.dump(svr, path_saving_svm)
joblib.dump(kr, path_saving_kr)
