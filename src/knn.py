import Element


def _calculate_distance(sequence_a, sequence_b):
    result = 0
    for i in range(0, len(sequence_a)):
        result += abs(sequence_a[i] - sequence_b[i])
    return result


def _calculate_error(set):
    sum = 0
    size = len(set)
    for e in set:
        sum += e.error
    return sum/size


def _calculate_weighted_error(set):
    sum_px = 0
    sum_p = 0
    for e in set:
        if e.distance == 0:
            e.distance = 0.0001
        sum_px += (e.error / e.distance)
        sum_p += e.distance
    return sum_px/sum_p


def _find_k_neighbors(input, samples, errors, k):   # to optimize
    result = []
    for i in range(0, len(samples)):
        result.append(Element.Element(_calculate_distance(input, samples[i]), errors[i][0]))
        if len(result) > k:
            result.sort(reverse=True)
            result = result[1:]
    return result


def _find_k_neighbors_weighted(input, weights, samples, errors, k):   # to optimize
    result = []
    input = input * weights
    for i in range(0, len(samples)):
        result.append(Element.Element(_calculate_distance(input, samples[i]), errors[i][0]))
        if len(result) > k:
            result.sort(reverse=True)
            result = result[1:]
    return result


def get_error_estimation(input, samples, errors, k, weighted):
    neighbors = _find_k_neighbors(input, samples, errors, k)
    if weighted:
        return _calculate_weighted_error(neighbors)
    else:
        return _calculate_error(neighbors)


def find_k_neighbors(input, samples, errors, k):   # to optimize
    result = []
    for i in range(0, len(samples)):
        result.append(Element.Element(_calculate_distance(input, samples[i]), errors[i][0], samples[i], errors[i]))
        if len(result) > k:
            result.sort(reverse=True)
            result = result[1:]

    result_i = []
    result_o = []
    for i in range(0, len(result)):
        result_i.append(result[i].input)
        result_o.append(result[i].output)

    return result_i, result_o


def get_error_estimation_weighted_on_input(input, weights, samples, errors, k, weighted):
    neighbors = _find_k_neighbors_weighted(input, weights, samples, errors, k)
    if weighted:
        return _calculate_weighted_error(neighbors)
    else:
        return _calculate_error(neighbors)