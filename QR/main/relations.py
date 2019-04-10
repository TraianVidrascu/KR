from main.utils import Magnitude, Derivative


class RelationType:
    POSITIVE = 1
    NEGATIVE = -1


class Relation:
    # Computes the derivative of the quantity with respect to the proportional relationship
    @staticmethod
    def compute_rules(quantity):
        relations = quantity.in_bound_relations

        if len(relations) == 0:
            return True
        derivative = quantity.derivative
        negative = 0
        zero = 0
        positive = 0
        for relation in relations:
            result = relation.compute_rule()
            if result < 0:
                negative += 1
            elif result > 0:
                positive += 1
            else:
                zero += 1

        if positive > 0 and negative == 0:
            return derivative is Derivative.POSITIVE
        elif negative > 0 and positive == 0:
            return derivative is Derivative.NEGATIVE
        if zero > 0 and negative == 0 and positive == 0:
            return derivative is Derivative.ZERO
        return True


class ProportionalRelation:
    def __init__(self, rel_type, quantity_1, quantity_2):
        self.rel_type = rel_type
        self.quantity_1 = quantity_1
        self.quantity_2 = quantity_2

    # Computes the derivative of the quantity with respect to the proportional relationship
    def compute_rule(self):
        rel_type = self.rel_type  # get the type of the relation positive or negative
        first_derivative = self.quantity_1.derivative  # get monotony of the first quantity
        expected_derivative = rel_type * first_derivative  # calculate the expected monotony for quantity 2
        return expected_derivative


class InfluenceRelation:
    def __init__(self, rel_type, quantity_1, quantity_2):
        self.rel_type = rel_type
        self.quantity_1 = quantity_1
        self.quantity_2 = quantity_2

    # Computes the derivative of the quantity with respect to the influence relationship
    def compute_rule(self):
        rel_type = self.rel_type
        first_magnitude = self.quantity_1.magnitude
        if first_magnitude > Magnitude.ZERO:
            expected_derivative = rel_type * Derivative.POSITIVE
        else:
            expected_derivative = Derivative.ZERO
        return expected_derivative
