

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