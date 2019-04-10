class Derivative:
    NEGATIVE = -1
    ZERO = 0
    POSITIVE = 1


# defining next possible derivatives values from current one
class DerivativeRules:
    derivative_rules = dict()
    derivative_rules[Derivative.NEGATIVE] = [Derivative.NEGATIVE, Derivative.ZERO]
    derivative_rules[Derivative.ZERO] = [Derivative.NEGATIVE, Derivative.ZERO, Derivative.POSITIVE]
    derivative_rules[Derivative.POSITIVE] = [Derivative.ZERO, Derivative.POSITIVE]


# Magnitudes used in our causal model 0 means zero, 1 means positive and 2 means max
class Magnitude:
    ZERO = 0
    MAX = 2
    POSITIVE = 1


# Defining possible magnitude from one state transition to another
class MagnitudeRules:
    magnitude_rules = dict()
    magnitude_rules[Magnitude.ZERO] = dict([(Derivative.NEGATIVE, [Magnitude.ZERO]),
                                            (Derivative.ZERO, [Magnitude.ZERO]),
                                            (Derivative.POSITIVE, [Magnitude.POSITIVE])])

    magnitude_rules[Magnitude.POSITIVE] = dict([(Derivative.NEGATIVE, [Magnitude.ZERO, Magnitude.POSITIVE]),
                                                (Derivative.ZERO, [Magnitude.POSITIVE]),
                                                (Derivative.POSITIVE, [Magnitude.POSITIVE, Magnitude.MAX])])

    magnitude_rules[Magnitude.MAX] = dict([(Derivative.NEGATIVE, [Magnitude.POSITIVE]),
                                           (Derivative.ZERO, [Magnitude.MAX]),
                                           (Derivative.POSITIVE, [Magnitude.MAX])])


class ValueSpace:
    INFLOW = [Magnitude.ZERO, Magnitude.POSITIVE]
    REST = [Magnitude.ZERO, Magnitude.POSITIVE, Magnitude.MAX]
    DERIVATIVE_SPACE = [Derivative.NEGATIVE, Derivative.ZERO, Derivative.POSITIVE]
