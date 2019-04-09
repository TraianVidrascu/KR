from main.utils import Derivative, Magnitude


class Quantity:
    def __init__(self, value_space, name, relations=None, constrains=None):
        self.name = name
        self.derivative = Derivative.ZERO
        self.magnitude = Magnitude.ZERO
        self.value_space = value_space
        self.relations = relations
        self.constrains = constrains
        if self.relations is None:
            self.relations = []
        if self.constrains is None:
            self.constrains = []

    def add_relation(self, relation):
        self.relations.append(relation)

    def add_constraint(self, constraint):
        self.constrains.append(constraint)

