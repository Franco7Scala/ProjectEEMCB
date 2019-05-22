from sklearn.externals import joblib
import Nation
import parser
import sys
import support
import knn
import warnings
import numpy


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


nation_id = sys.argv[1]
source_id = int(sys.argv[2])
input = numpy.asanyarray([float(i) for i in sys.argv[3].split(" ")]).reshape(1, -1)
verbose = bool(sys.argv[4])

nation = Nation.load_nation(nation_id)

path_model = nation.sources[source_id].path_model

if verbose:
    support.colored_print("Loading model...", "green")

model = joblib.load(path_model)

if verbose:
    support.colored_print("Making prediction...", "green")

output = model.predict(input)

if verbose:
    support.colored_print("Estimating error...", "green")

training_set_error_input, training_set_error_output, _, _ = parser.parse_data(nation.sources[source_id].path_training_set_error)
error = knn.get_error_estimation(input[0], training_set_error_input, training_set_error_output, nation.sources[source_id].best_k, False)

if verbose:
    support.colored_print("Showing results...", "green")

support.colored_print("Prediction: %.2lf\nAbsolute error (estimated): %.2lf" % (output[0], error), "blue")
support.colored_print("Completed!", "pink")
