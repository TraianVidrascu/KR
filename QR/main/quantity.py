from main.relations import Relation
from main.utils import Derivative, Magnitude, ValueSpace


class Quantity:
    def __init__(self, value_space, name, derivative=Derivative.ZERO, magnitude=Magnitude.ZERO):
        self.name = name
        self.derivative = derivative
        self.magnitude = magnitude
        self.value_space = value_space
        self.in_bound_relations = []

    def get_all_states(self):
        all_quantity_states = []
        for derivative in ValueSpace.DERIVATIVE_SPACE:
            for magnitude in self.value_space:
                pair = (derivative, magnitude)
                all_quantity_states.append(pair)
        return all_quantity_states

    def add_relation(self, relation):
        self.in_bound_relations.append(relation)

    def respects_relations(self):
        result = Relation.compute_rules(self)
        return result

    def set_value(self, combination):
        self.derivative = combination[0]
        self.magnitude = combination[1]
