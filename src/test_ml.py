from __future__ import division
from sklearn.externals import joblib
import numpy
import Support
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


filename = "/Users/francesco/Desktop/results_svr/svm_"
output_quantity = 6
samples_quantity = 5
input = numpy.asarray([[261, 0, 0, 0.0, 3030.0, 384.0, 151.0, 30407.0, -3277.0, 83.17, 29.464, 20.79],
                       [265, 1, 19, 0.0, 6505.0, 403.0, 594.0, 37066.0, -4461.0, 83.17, 29.216, 20.79],
                       [273, 1, 10, 6797.0, 2105.0, 409.0, 1983.0, 27669.0, -2856.0, 83.17, 28.867, 20.79],
                       [277, 0, 1, 0.0, 1522.0, 382.0, 3313.0, 26680.0, -5624.0, 83.17, 28.951, 20.79],
                       [282, 0, 21, 0.0, 3633.0, 406.0, 752.0, 37738.0, -6376.326, 83.17, 28.098, 20.79]])
expected_outputs = numpy.asarray([[236.0, 10946.0, 4284.0, 79.0, 37.0, 7269.0],
                                  [220.0, 11207.0, 4456.0, 119.0, 41.0, 8497.0],
                                  [232.0, 3459.0, 3737.0, 52.0, 37.0, 5357.0],
                                  [231.0, 6422.0, 3158.0, 20.0, 42.0, 5388.0],
                                  [231.0, 13078.0, 4180.0, 62.0, 38.0, 8765.0]])
#verifying
for output_selected in range(0, output_quantity):
    model = joblib.load(filename + str(output_selected) + ".joblib")
    Support.colored_print("Verifying output n: " + str(output_selected), "blue")
    for sample_selected in range(0, samples_quantity):
        real_output = model.predict(input[sample_selected].reshape(1, -1))
        Support.colored_print("Sample n: " + str(sample_selected), "pink")
        Support.colored_print("Expected output: " + str(expected_outputs[sample_selected][output_selected]), "green")
        Support.colored_print("Real output: " + str(real_output), "green")
Support.colored_print("Done!", "red")

