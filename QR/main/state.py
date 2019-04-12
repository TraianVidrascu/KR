from main.constraints import EqualConstraint
from main.quantity import Quantity
from main.relations import ProportionalRelation, RelationType, InfluenceRelation
from main.utils import ValueSpace, Magnitude, Derivative

OUTFLOW = "outflow"
PRESSURE = "pressure"
HEIGHT = "height"
VOLUME = "volume"
INFLOW = "inflow"


class Container:
    INDEX = 0
    NAME = 1
    def __init__(self):
        self.quantities = []
        self.constraints = []
        self.id = Container.get_id()
        self.name = ""
        self.init()

    def has_valid_values(self):
        for quantity in self.quantities:
            if quantity.magnitude is Magnitude.ZERO and quantity.derivative is Derivative.NEGATIVE:
                return False
        return True

    def repsects_constraints(self):
        for constraint in self.constraints:
            result = constraint.check_rule()
            if result is False:
                return False
        return True

    def respect_relations(self):
        for quantity in self.quantities:
            result = quantity.respects_relations()
            if result is False:
                return False
        return True

    def get_all_combinations(self):
        all_states = []
        for quantity in self.quantities:
            all_quantity_states = quantity.get_all_states()
            all_states.append(all_quantity_states)
        return all_states

    def set_values(self, combination):
        for index, combination in enumerate(combination):
            self.quantities[index].set_value(combination)

    def init(self):
        # defining quantities
        inflow = Quantity(ValueSpace.INFLOW, INFLOW)
        volume = Quantity(ValueSpace.REST, VOLUME)
        height = Quantity(ValueSpace.REST, HEIGHT)
        pressure = Quantity(ValueSpace.REST, PRESSURE)
        outflow = Quantity(ValueSpace.REST, OUTFLOW)

        # defining influential relations
        i1 = InfluenceRelation(RelationType.POSITIVE, inflow, volume)
        i2 = InfluenceRelation(RelationType.NEGATIVE, outflow, volume)
        volume.add_relation(i1)
        volume.add_relation(i2)

        # defining proportional relations
        p1 = ProportionalRelation(RelationType.POSITIVE, volume, height)
        p2 = ProportionalRelation(RelationType.POSITIVE, height, pressure)
        p3 = ProportionalRelation(RelationType.POSITIVE, pressure, outflow)
        height.add_relation(p1)
        pressure.add_relation(p2)
        outflow.add_relation(p3)

        # defining constraints
        c1 = EqualConstraint(volume, Magnitude.MAX, height, Magnitude.MAX)
        c2 = EqualConstraint(volume, Magnitude.ZERO, height, Magnitude.ZERO)
        c3 = EqualConstraint(height, Magnitude.MAX, pressure, Magnitude.MAX)
        c4 = EqualConstraint(height, Magnitude.ZERO, pressure, Magnitude.ZERO)
        c5 = EqualConstraint(pressure, Magnitude.MAX, outflow, Magnitude.MAX)
        c6 = EqualConstraint(pressure, Magnitude.ZERO, outflow, Magnitude.ZERO)

        # adding constraints
        self.constraints.append(c1)
        self.constraints.append(c2)
        self.constraints.append(c3)
        self.constraints.append(c4)
        self.constraints.append(c5)
        self.constraints.append(c6)

        # adding quantities to the container
        self.quantities.append(inflow)
        self.quantities.append(volume)
        self.quantities.append(height)
        self.quantities.append(pressure)
        self.quantities.append(outflow)

    @classmethod
    def get_id(cls):
        Container.INDEX += 1
        return Container.INDEX
