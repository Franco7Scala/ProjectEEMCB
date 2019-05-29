import support
import json


class Nation:
    def __init__(self, id, name = "", base_path_datas = "", path_training_set_prediction_rf = "", path_training_set_prediction_wp = "", path_training_set_prediction_wpwl = "", path_training_set_prediction_wpaw = ""):
        self.id = id
        self.name = name
        self.base_path_datas = base_path_datas
        self.path_training_set_prediction_rf = path_training_set_prediction_rf
        self.path_training_set_prediction_wp = path_training_set_prediction_wp
        self.path_training_set_prediction_wpwl = path_training_set_prediction_wpwl
        self.path_training_set_prediction_wpaw = path_training_set_prediction_wpaw
        self.indexes_inputs = []
        self.indexes_outputs = []
        self.sources = []

    def __str__(self):
        sources = ""
        for source in self.sources:
            sources += "\n" + str(source)
        return "id: " + str(self.id) + "\n" + \
               "name: " + str(self.name) + "\n" + \
               "base_path_datas: " + str(self.base_path_datas) + "\n" + \
               "path_training_set_prediction_rf: " + str(self.path_training_set_prediction_rf) + "\n" + \
               "path_training_set_prediction_wp: " + str(self.path_training_set_prediction_wp) + "\n" + \
               "path_training_set_prediction_wpwl: " + str(self.path_training_set_prediction_wpwl) + "\n" + \
               "path_training_set_prediction_wpaw: " + str(self.path_training_set_prediction_wpaw) + "\n" + \
               "indexes_inputs: " + str(self.indexes_inputs) + "\n" + \
               "indexes_outputs: " + str(self.indexes_outputs) + "\n" + \
               "\nsources: " + sources


class Production:
    def __init__(self, id, name = "", path_model = "", path_training_set_prediction = "", path_training_set_error = "", path_statistics_training = "", best_model = 0, best_k = 0, k_weighted = False):
        self.id = id
        self.name = name
        self.best_k = best_k
        self.k_weighted = k_weighted
        self.best_model = best_model
        self.path_model = path_model
        self.path_training_set_prediction = path_training_set_prediction
        self.path_training_set_error = path_training_set_error
        self.path_statistics_training = path_statistics_training

    def __str__(self):
        return "id: " + str(self.id) + "\n" + \
               "name: " + str(self.name) + "\n" + \
               "best_k: " + str(self.best_k) + "\n" + \
               "k_weighted: " + str(self.k_weighted) + "\n" + \
               "best_model: " + str(self.best_model) + "\n" + \
               "path_model: " + self.path_model + "\n" \
               "path_training_set_prediction: " + str(self.path_training_set_prediction) + "\n" + \
               "path_training_set_error: " + self.path_training_set_error + "\n" \
               "path_statistics_training: " + self.path_statistics_training + "\n"


def load_nation(id):
    result = Nation(id)
    with open(support.BASE_PATH_NATIONS + "/" + str(id) + ".json", "r") as input_file:
        dict = json.load(input_file)

    result.id = int(dict["nation"]["id"])
    result.name = dict["nation"]["name"]
    result.base_path_datas = dict["nation"]["base_path_datas"]
    result.path_training_set_prediction_rf = dict["nation"]["path_training_set_prediction_rf"]
    result.path_training_set_prediction_wp = dict["nation"]["path_training_set_prediction_wp"]
    result.path_training_set_prediction_wpwl = dict["nation"]["path_training_set_prediction_wpwl"]
    result.path_training_set_prediction_wpaw = dict["nation"]["path_training_set_prediction_wpaw"]
    result.indexes_inputs = []
    for _, e in enumerate(dict["nation"]["indexes_inputs"].split()):
        result.indexes_inputs.append(float(e.strip()))

    result.indexes_outputs = []
    for _, e in enumerate(dict["nation"]["indexes_outputs"].split()):
        result.indexes_outputs.append(float(e.strip()))

    for entry in dict["nation"]["sources"]["production"]:
        production = Production(entry["id"])
        production.name = entry["name"]
        production.best_k = int(entry["best_k"])
        production.k_weighted = bool(entry["k_weighted"])
        production.best_model = int(entry["best_model"])
        production.path_model = entry["path_model"]
        production.path_training_set_prediction = entry["path_training_set_prediction"]
        production.path_training_set_error = entry["path_training_set_error"]
        production.path_statistics_training = entry["path_statistics_training"]
        result.sources.append(production)

    return result
