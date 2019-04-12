class Derivative:
    NEGATIVE = -1
    ZERO = 0
    POSITIVE = 1


# Magnitudes used in our causal model 0 means zero, 1 means positive and 2 means max
class Magnitude:
    ZERO = 0
    MAX = 2
    POSITIVE = 1


class ValueType:
    INTERVALS = [Magnitude.POSITIVE]
    POINTS = [Magnitude.ZERO, Magnitude.MAX]


class Names:
    derivative_names = dict()
    derivative_names[Derivative.NEGATIVE] = "-"
    derivative_names[Derivative.POSITIVE] = "+"
    derivative_names[Derivative.ZERO] = "0"
    magnitude_names = dict()
    magnitude_names[Magnitude.MAX] = "Max"
    magnitude_names[Magnitude.POSITIVE] = "Positive"
    magnitude_names[Magnitude.ZERO] = "Zero"


# defining next possible derivatives values from current one
class DerivativeRules:
    derivative_rules = dict()
    derivative_rules[Derivative.NEGATIVE] = dict([(Magnitude.ZERO, [(Magnitude.ZERO, Derivative.ZERO)]),
                                                  (Magnitude.POSITIVE, [(Magnitude.POSITIVE, Derivative.NEGATIVE),
                                                                        (Magnitude.POSITIVE, Derivative.ZERO),
                                                                        (Magnitude.ZERO, Derivative.ZERO)]),
                                                  (Magnitude.MAX, [(Magnitude.POSITIVE, Derivative.NEGATIVE)])])
    derivative_rules[Derivative.ZERO] = dict(
        [(Magnitude.ZERO, [(Magnitude.ZERO, Derivative.ZERO), (Magnitude.ZERO, Derivative.POSITIVE)]),
         (Magnitude.POSITIVE, [(Magnitude.POSITIVE, Derivative.ZERO), (Magnitude.POSITIVE, Derivative.NEGATIVE),
                               (Magnitude.POSITIVE, Derivative.POSITIVE)]),
         (Magnitude.MAX, [(Magnitude.MAX, Derivative.ZERO), (Magnitude.MAX, Derivative.NEGATIVE)])])
    derivative_rules[Derivative.POSITIVE] = dict([(Magnitude.ZERO, [(Magnitude.POSITIVE, Derivative.POSITIVE)]),
                                                  (Magnitude.POSITIVE, [(Magnitude.POSITIVE, Derivative.POSITIVE),
                                                                        (Magnitude.POSITIVE, Derivative.ZERO),
                                                                        (Magnitude.MAX, Derivative.ZERO),
                                                                        (Magnitude.MAX, Derivative.POSITIVE)]),
                                                  (Magnitude.MAX, [(Magnitude.MAX, Derivative.ZERO),
                                                                   (Magnitude.MAX, Derivative.POSITIVE)])])


class InflowBehaviour:
    inflow_behaviour = dict()
    inflow_behaviour[Derivative.POSITIVE] = dict([(Magnitude.ZERO, [(Magnitude.POSITIVE, Derivative.POSITIVE)]),
                                                  (Magnitude.POSITIVE, [(Magnitude.POSITIVE, Derivative.POSITIVE),
                                                                        (Magnitude.POSITIVE, Derivative.ZERO)])])
    inflow_behaviour[Derivative.ZERO] = dict([(Magnitude.ZERO, [(Magnitude.ZERO, Derivative.ZERO)]),
                                              (Magnitude.POSITIVE, [(Magnitude.POSITIVE, Derivative.NEGATIVE),
                                                                    (Magnitude.ZERO, Derivative.ZERO)])])
    inflow_behaviour[Derivative.NEGATIVE] = dict([(Magnitude.ZERO, [(Magnitude.ZERO, Derivative.ZERO)]),
                                                  (Magnitude.POSITIVE, [(Magnitude.POSITIVE, Derivative.NEGATIVE),
                                                                        (Magnitude.ZERO, Derivative.ZERO)])])


# Defining possible magnitude from one state transition to another
class MagnitudeRules:
    magnitude_rules = dict()
    magnitude_rules[Magnitude.ZERO] = dict([(Derivative.NEGATIVE, [Magnitude.ZERO]),
                                            (Derivative.ZERO, [Magnitude.ZERO]),
                                            (Derivative.POSITIVE, [Magnitude.POSITIVE])])

    magnitude_rules[Magnitude.POSITIVE] = dict([(Derivative.NEGATIVE, [Magnitude.ZERO,
                                                                       Magnitude.ZERO,
                                                                       Magnitude.POSITIVE]),
                                                (Derivative.ZERO, [Magnitude.POSITIVE]),
                                                (Derivative.POSITIVE, [Magnitude.POSITIVE, Magnitude.MAX])])

    magnitude_rules[Magnitude.MAX] = dict([(Derivative.NEGATIVE, [Magnitude.POSITIVE]),
                                           (Derivative.ZERO, [Magnitude.MAX]),
                                           (Derivative.POSITIVE, [Magnitude.MAX])])


class ValueSpace:
    INFLOW = [Magnitude.ZERO, Magnitude.POSITIVE]
    REST = [Magnitude.ZERO, Magnitude.POSITIVE, Magnitude.MAX]
    DERIVATIVE_SPACE = [Derivative.NEGATIVE, Derivative.ZERO, Derivative.POSITIVE]
