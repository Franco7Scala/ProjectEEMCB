import Element


def _calculate_distance(sequence_a, sequence_b):
    result = 0
    for i in range(0, len(sequence_a)):
        result += abs(sequence_a[i] - sequence_b[i])
    return result


def find_k_neighbors(input, samples, errors, k):
    result = []
    for i in range(0, len(samples)):
        if len(result) < k:
            result.append(Element(_calculate_distance(input, samples[i]), errors[i][0]))
        else:
            max_distance = max(result)
            current_distance = _calculate_distance(input, samples[i])
            if current_distance < max_distance.distance:
                max_index = result.index(max_distance)
                result[max_index] = Element(_calculate_distance(input, samples[i]), errors[i][0])
    return result


def calculate_error(set):
    sum = 0
    size = len(set)
    for e in set:
        sum += e.error
    return sum/size


def get_error_estimation(input, samples, errors, k):
    return calculate_error(find_k_neighbors(input, samples, errors, k))