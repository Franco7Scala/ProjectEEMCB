from __future__ import division
from sklearn.externals import joblib
import numpy
import Support
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


filename = "/Users/francesco/Desktop/results_svr_v2_22/svm_"
output_quantity = 6
samples_quantity = 5
input = numpy.asarray([[269, 0, 18, 532.0, 5938.0, 346.0, 5449.0, 39040.0, -3990.0, 83.17, 83.17, 83.17],
                       [267, 0, 22, 0.0, 3616.0, 325.0, 3954.0, 35170.0, -4280.0, 83.17, 83.17, 83.17],
                       [266, 1, 9, 5037.0, 2928.0, 381.0, 237.0, 28329.0, 0.0, 83.17, 83.17, 83.17],
                       [264, 0, 15, 5788.0, 4926.0, 406.0, 911.0, 43010.0, -4463.0, 83.17, 83.17, 83.17],
                       [262, 0, 2, 0.0, 2139.0, 365.0, 184.0, 27794.0, -4477.0, 83.17, 83.17, 83.17]])
expected_outputs = numpy.asarray([[210.0, 10616.0, 2832.0, 112.0, 36.0, 8573.0],
                                  [212.0, 10953.0, 3328.0, 60.0, 49.0, 7869.0],
                                  [216.0, 6045.0, 3515.0, 21.0, 49.0, 6052.0],
                                  [222.0, 13667.0, 3926.0, 60.0, 41.0, 8011.0],
                                  [244.0, 9421.0, 4382.0, 74.0, 44.0, 5744.0]])
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

