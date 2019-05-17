

class Element:
    def __init__(self, id, path_model_base, path_training_set_error, path_training_set_predition, best_k, statistics = None):
        self.id = id
        self.path_model_base = path_model_base
        self.path_training_set_error = path_training_set_error
        self.path_training_set_predition = path_training_set_predition
        self.best_k = best_k
        self.statistics = statistics

    def get_training_set_error_input(self):
        return None

    def get_training_set_error_output(self):
        return None
