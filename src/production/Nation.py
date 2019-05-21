import support
import json


class Nation:
    def __init__(self, id, name = "", path_datas = "", path_training_set_prediction = "", path_test_set_prediction = "", statistics = None):
        self.id = id
        self.name = name
        self.path_datas = path_datas
        self.statistics = statistics
        self.path_training_set_prediction = path_training_set_prediction
        self.path_test_set_prediction = path_test_set_prediction
        self.sources = []

    def __str__(self):
        sources = ""
        for source in self.sources:
            sources += "\n" + str(source)
        return "id: " + str(self.id) + "\n" + \
               "name: " + str(self.name) + "\n" + \
               "statistics: " + str(self.statistics) + "\n" + \
               "path_datas: " + str(self.path_datas) + "\n" + \
               "path_training_set_prediction: " + str(self.path_training_set_prediction) + "\n" + \
               "path_test_set_prediction: " + str(self.path_test_set_prediction) + "\n" + \
               "\nsources: " + sources


class Production:
    def __init__(self, id, name = "", path_training_set_error = "", path_statistics = "", best_model = 0, best_k = 0):
        self.id = id
        self.name = name
        self.best_k = best_k
        self.best_model = best_model
        self.path_training_set_error = path_training_set_error
        self.path_statistics = path_statistics

    def __str__(self):
        return "id: " + str(self.id) + "\n" + \
               "name: " + str(self.name) + "\n" + \
               "best_k: " + str(self.best_k) + "\n" + \
               "best_model: " + str(self.best_model) + "\n" + \
               "path_training_set_error: " + self.path_training_set_error + "\n" \
               "path_statistics: " + self.path_statistics + "\n"


def load_nation(id):
    result = Nation(id)
    with open(support.BASE_PATH_NATIONS + "/" + str(id) + ".json", "r") as input_file:
        dict = json.load(input_file)

    result.id = int(dict["nation"]["id"])
    result.name = dict["nation"]["name"]
    result.path_datas = dict["nation"]["path_datas"]
    result.statistics = dict["nation"]["statistics"]
    result.path_training_set_prediction = dict["nation"]["path_training_set_prediction"]
    result.path_test_set_prediction = dict["nation"]["path_test_set_prediction"]
    for entry in dict["nation"]["sources"]["production"]:
        production = Production(entry["id"])
        production.name = entry["name"]
        production.name = int(entry["best_k"])
        production.name = int(entry["best_model"])
        production.path_training_set_error = entry["path_training_set_error"]
        production.path_statistics = entry["path_statistics"]
        result.sources.append(production)

    return result