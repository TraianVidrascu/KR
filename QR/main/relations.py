from main.utils import Magnitude, Derivative


class RelationType:
    POSITIVE = 1
    NEGATIVE = -1


# class Relation:
#     # Computes the derivative of the quantity with respect to the proportional relationship
#     @staticmethod
#     def compute_rules(proportional_relations):
#         negative = 0
#         zero = 0
#         positive = 0
#         for proportional_relation in proportional_relations:
#             result = proportional_relations.compute_rule(proportional_relation)
#             if result < 0:
#                 negative += 1
#             elif result > 0:
#                 positive += 1
#             else:
#                 zero += 1
#         if positive > 0 and negative > 0:
#             return None
#         elif positive > 0:
#             return Derivative.POSITIVE
#         elif negative > 0:
#             return Derivative.NEGATIVE
#         return Derivative.ZERO


class ProportionalRelation:
    def __init__(self, rel_type, quantity_1, quantity_2):
        self.rel_type = rel_type
        self.quantity_1 = quantity_1
        self.quantity_2 = quantity_2

    # Computes the derivative of the quantity with respect to the proportional relationship
    def check_rule(self):
        rel_type = self.rel_type
        first_derivative = self.quantity_1.derivative
        second_derivative = self.quantity_2.derivative
        expected_derivative = rel_type * first_derivative
        if second_derivative == expected_derivative:
            return True
        return False


class InfluenceRelation:
    def __init__(self, rel_type, quantity_1, quantity_2):
        self.rel_type = rel_type
        self.quantity_1 = quantity_1
        self.quantity_2 = quantity_2

    # Computes the derivative of the quantity with respect to the influence relationship
    def check_rule(self):
        rel_type = self.rel_type
        first_magnitude = self.quantity_1.magnitude
        second_derivative = self.quantity_2.derivative
        expected_derivative = rel_type * Derivative.POSITIVE if first_magnitude > Magnitude.ZERO else Derivative.ZERO
        if expected_derivative == second_derivative:
            return True
        return False
