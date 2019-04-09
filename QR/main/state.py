from main.constraints import EqualConstraint
from main.quantity import Quantity
from main.relations import ProportionalRelation, RelationType, InfluenceRelation
from main.utils import ValueSpace, Magnitude

OUTFLOW = "outflow"
PRESSURE = "pressure"
HEIGHT = "height"
VOLUME = "volume"
INFLOW = "inflow"


class Container:
    def __init__(self):
        self.quantities = []
        self.initialize()

    def initialize(self):
        # defining quantities
        inflow = Quantity(ValueSpace.INFLOW, INFLOW)
        volume = Quantity(ValueSpace.REST, VOLUME)
        height = Quantity(ValueSpace.REST, HEIGHT)
        pressure = Quantity(ValueSpace.REST, PRESSURE)
        outflow = Quantity(ValueSpace.REST, OUTFLOW)

        # defining influential relations
        InfluenceRelation(RelationType.POSITIVE, inflow, volume)
        InfluenceRelation(RelationType.POSITIVE, outflow, volume)

        # defining proportional relations
        ProportionalRelation(RelationType.POSITIVE, volume, height)
        ProportionalRelation(RelationType.POSITIVE, height, pressure)
        ProportionalRelation(RelationType.POSITIVE, pressure, outflow)

        # defining constraints
        EqualConstraint(volume, Magnitude.MAX, height, Magnitude.MAX)
        EqualConstraint(volume, Magnitude.ZERO, height, Magnitude.ZERO)
        EqualConstraint(height, Magnitude.MAX, pressure, Magnitude.MAX)
        EqualConstraint(height, Magnitude.ZERO, pressure, Magnitude.ZERO)
        EqualConstraint(pressure, Magnitude.MAX, outflow, Magnitude.MAX)
        EqualConstraint(pressure, Magnitude.ZERO, outflow, Magnitude.ZERO)

        # adding quantities to the container
        self.quantities.append(inflow)
        self.quantities.append(volume)
        self.quantities.append(height)
        self.quantities.append(pressure)
        self.quantities.append(outflow)

Container()