class EqualConstraint:
    def __init__(self, first_quantity, first_value, second_quantity, second_value):
        self.first_quantity = first_quantity
        self.first_value = first_value
        self.second_quantity = second_quantity
        self.second_value = second_value

    def check_rule(self):
        first_magnitude = self.first_quantity.magnitude
        second_magnitude = self.second_quantity.magnitude
        if first_magnitude == self.first_value and second_magnitude == self.second_value:
            return True
        return False

    def apply_rule(self):
        first_magnitude = self.first_quantity.magnitude
        second_magnitude = self.second_quantity.magnitude
        if first_magnitude == self.first_value:
            self.second_quantity.magnitude = first_magnitude
        if second_magnitude == self.second_value:
            self.first_quantity.magnitude = second_magnitude

