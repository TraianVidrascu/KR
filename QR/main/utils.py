class Derivative:
    NEGATIVE = -1
    ZERO = 0
    POSITIVE = 1


# defining next possible derivatives values from current one
class ProportionalRules:
    NEXT_POSSIBLE_FROM_NEGATIVE_DERIVATIVE = [Derivative.NEGATIVE, Derivative.ZERO]
    NEXT_POSSIBLE_FROM_ZERO_DERIVATIVE = [Derivative.NEGATIVE, Derivative.ZERO, Derivative.POSITIVE]
    NEXT_POSSIBLE_FROM_POSITIVE_DERIVATIVE = [Derivative.ZERO, Derivative.POSITIVE]


class ParabolicFunction:
    INITIAL = []
    MAXIMUM = []
    INCREASING = []
    DECREASING = []
    FINAL = []

    # defining function transition rules for first derivative
    INITIAL = ([INCREASING], Derivative.ZERO)
    INCREASING = ([INCREASING, MAXIMUM], Derivative.POSITIVE)
    MAXIMUM = ([DECREASING], Derivative.ZERO)
    DECREASING = ([DECREASING, FINAL], Derivative.NEGATIVE)
    FINAL = ([], Derivative.ZERO)


# Magnitudes used in our causal model 0 means zero, 1 means positive and 2 means max
class Magnitude:
    ZERO = 0
    MAX = 2
    POSITIVE = 1


class ValueSpace:
    INFLOW = [Magnitude.ZERO, Magnitude.POSITIVE]
    REST = [Magnitude.ZERO, Magnitude.POSITIVE, Magnitude.MAX]
    DERIVATIVE_SPACE = [Derivative.NEGATIVE, Derivative.ZERO, Derivative.POSITIVE]
