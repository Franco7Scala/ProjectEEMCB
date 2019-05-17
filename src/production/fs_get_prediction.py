from sklearn.externals import joblib
import Nation
import sys
import support
import knn


nation_id = sys.argv[1]
source_id = int(sys.argv[2])
input = sys.argv[3]
verbose = bool(sys.argv[4])

nation = Nation()                     # TODO load info

path_model = nation.path_model_base + "/" + nation_id + "/model_" + str(source_id) + ".joblib"

if verbose:
    support.colored_print("Loading model...", "green")

model = joblib.load(path_model)

if verbose:
    support.colored_print("Making prediction...", "green")

output = model.predict(input)

if verbose:
    support.colored_print("Estimating error...", "green")

error = knn.get_error_estimation(input, nation.get_training_set_error_input(), nation.get_training_set_error_output(), nation.best_k, False)

if verbose:
    support.colored_print("Showing results...", "green")

support.colored_print("Output: " + str(output) + " Error: " + str(error), "pink")

