import support
import json


class Nation:
    def __init__(self, id, name = "", base_path_datas = "", path_training_set_prediction = ""):
        self.id = id
        self.name = name
        self.base_path_datas = base_path_datas
        self.path_training_set_prediction = path_training_set_prediction
        self.sources = []

    def __str__(self):
        sources = ""
        for source in self.sources:
            sources += "\n" + str(source)
        return "id: " + str(self.id) + "\n" + \
               "name: " + str(self.name) + "\n" + \
               "base_path_datas: " + str(self.base_path_datas) + "\n" + \
               "path_training_set_prediction: " + str(self.path_training_set_prediction) + "\n" + \
               "\nsources: " + sources


class Production:
    def __init__(self, id, name = "", path_model = "", path_training_set_error = "", path_statistics_training = "", path_statistics_error = "", best_model = 0, best_k = 0):
        self.id = id
        self.name = name
        self.best_k = best_k
        self.best_model = best_model
        self.path_model = path_model
        self.path_training_set_error = path_training_set_error
        self.path_statistics_training = path_statistics_training
        self.path_statistics_error = path_statistics_error

    def __str__(self):
        return "id: " + str(self.id) + "\n" + \
               "name: " + str(self.name) + "\n" + \
               "best_k: " + str(self.best_k) + "\n" + \
               "best_model: " + str(self.best_model) + "\n" + \
               "path_model: " + self.path_model + "\n" \
               "path_training_set_error: " + self.path_training_set_error + "\n" \
               "path_statistics_training: " + self.path_statistics_training + "\n" \
               "path_statistics_error: " + self.path_statistics_error + "\n"


def load_nation(id):
    result = Nation(id)
    with open(support.BASE_PATH_NATIONS + "/" + str(id) + ".json", "r") as input_file:
        dict = json.load(input_file)

    result.id = int(dict["nation"]["id"])
    result.name = dict["nation"]["name"]
    result.base_path_datas = dict["nation"]["base_path_datas"]
    result.path_training_set_prediction = dict["nation"]["path_training_set_prediction"]
    for entry in dict["nation"]["sources"]["production"]:
        production = Production(entry["id"])
        production.name = entry["name"]
        production.best_k = int(entry["best_k"])
        production.best_model = int(entry["best_model"])
        production.path_model = entry["path_model"]
        production.path_training_set_error = entry["path_training_set_error"]
        production.path_statistics_training = entry["path_statistics_training"]
        production.path_statistics_error = entry["path_statistics_error"]
        result.sources.append(production)

    return result
