from main.utils import Derivative, Magnitude


class Quantity:
    def __init__(self, value_space, relations=None, constrains=None):
        self.derivative = Derivative.ZERO
        self.magnitude = Magnitude.ZERO
        self.value_space = value_space
        self.relations = relations
        self.constrains = constrains
        if self.relations is None:
            self.relations = []
        if self.constrains is None:
            self.constrains = []

