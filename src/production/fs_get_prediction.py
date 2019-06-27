from sklearn.externals import joblib
import nation
import parser
import sys
import support
import knn
import warnings
import numpy


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


if len(sys.argv) == 1 or sys.argv[1] == "help":
    support.colored_print("Usage:\n\t-parameter 1: nation code (string)\n\t-parameter 2: source id (int)\n\t-parameter 3: input (array)\n\t-parameter 4: verbose (bool)", "red")
    sys.exit(0)

nation_code = sys.argv[1]
source_id = int(sys.argv[2])
input = numpy.asanyarray([float(i) for i in sys.argv[3].split(" ")]).reshape(1, -1)
verbose = bool(sys.argv[4])

nation = nation.load_nation(nation_code)
path_model = nation.base_path_datas + nation.sources[source_id].path_model
if verbose:
    support.colored_print("Loading model...", "green")

model = joblib.load(path_model)

if verbose:
    support.colored_print("Making prediction...", "green")

output = model.predict(input)
if verbose:
    support.colored_print("Estimating error...", "green")

training_set_error_input, training_set_error_output, _, _ = parser.parse_data(nation.base_path_datas + nation.sources[source_id].path_training_set_error)
error = knn.get_error_estimation(input[0], training_set_error_input, training_set_error_output, nation.sources[source_id].best_k, nation.sources[source_id].k_weighted)
if verbose:
    support.colored_print("Showing results...", "green")

support.colored_print("Prediction: %.2lf\nRelative error (estimated): %.2lf %%" % (output[0], error), "blue")
support.colored_print("Completed!", "pink")
