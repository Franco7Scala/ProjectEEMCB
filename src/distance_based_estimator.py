import Support
import Parser
import sys
import numpy
from sklearn.externals import joblib


class Element:
    def __init__(self, distance, error):
        self.distance = distance
        self.error = error

    def __lt__(self, other):
        return self.distance < other.distance

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        return self.distance == other.distance

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "error:{}, distance:{}".format(self.error, self.distance)


def calculate_distance(sequence_a, sequence_b):
    result = 0
    for i in range(0, len(sequence_a)):
        result += abs(sequence_a[i] - sequence_b[i])
    return result

def find_k_neighbors(input, samples, errors, k):
    result = []
    for i in range(0, len(samples)):
        if len(result) < k:
            result.append(Element(calculate_distance(input, samples[i]), errors[i][0]))
        else:
            max_distance = max(result)
            current_distance = calculate_distance(input, samples[i])
            if current_distance < max_distance.distance:
                max_index = result.index(max_distance)
                result[max_index] = Element(calculate_distance(input, samples[i]), errors[i][0])
    return result


def calculate_error(set):
    sum = 0
    size = len(set)
    for e in set:
        sum += e.error
    return sum/size


if __name__ == '__main__':
    if len(sys.argv) != 6:
        k = 20
        given_input = [float(x) for x in "277.000000 0.000000 5.000000 0.000000 1753.000000 398.000000 2855.000000 27313.000000 -5612.000000 83.170000 28.951000 20.790000 212.000000 6799.000000 3494.000000 78.000000 39.000000 6010.000000".split(' ')]
        given_output = 232.0
        given_error = 5.989121
        path_model = "/Users/francesco/Desktop/Cose da Sistemare/best_predictors/all/fossil_coal.joblib"
        path_samples = "/Users/francesco/Desktop/Cose da Sistemare/datas/error/training_sets/training_set_fossil_coal_error.txt"
    else:
        k = int(sys.argv[1])
        given_input = [float(x) for x in sys.argv[2].split(' ')]
        given_output = float(sys.argv[3])
        given_error = float(sys.argv[4])
        path_model = sys.argv[5]
        path_samples = sys.argv[6]

    model = joblib.load(path_model)
    given_samples, given_errors, _, _ = Parser.parse_data(path_samples, 0)

    prediction = model.predict((numpy.asarray(given_input)).reshape(1, -1))

    Support.colored_print("model output: " + str(prediction), "blue")
    Support.colored_print("real output: " + str(given_output), "blue")

    errors = find_k_neighbors(given_input, given_samples, given_errors, k)
    error = calculate_error(errors)

    Support.colored_print("distance based error: " + str(error), "red")
    Support.colored_print("real error: " + str(given_error), "red")

    Support.colored_print("Completed!", "pink")










