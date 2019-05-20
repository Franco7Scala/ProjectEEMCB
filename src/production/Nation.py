import support


class Nation:
    def __init__(self, id, path_datas = "", path_training_set_error = "", path_training_set_prediction = "", best_k = 0, best_model = 0, statistics = None):
        self.id = id
        self.path_datas = path_datas
        self.best_k = best_k
        self.best_model = best_model
        self.statistics = statistics
        self.path_training_set_error = path_training_set_error
        self.path_training_set_prediction = path_training_set_prediction


def load_nation(id):
    result = Nation(id)
    with open(support.BASE_PATH_NATIONS + "/" + str(id) + ".txt", "r") as input_file:
        result.path_datas = input_file[1]
        result.path_training_set_error = input_file[2]
        result.path_training_set_prediction = input_file[3]
        result.best_k = int(input_file[4])
        result.best_model = int(input_file[5])

    return result