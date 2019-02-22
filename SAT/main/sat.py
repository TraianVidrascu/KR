import copy


class Clause:
    id = 0

    def __init__(self):
        self.clause_id = Clause.get_clause_id()
        self.variables = []

    @staticmethod
    def get_clause_id():
        Clause.id += 1
        return Clause.id

    def get_value(self, literals):
        for variable in self.variables:
            key = abs(variable)
            logical_value = literals[key].value
            if logical_value is not None:
                if variable > 0 and logical_value:
                    return True
                elif variable < 0 and not logical_value:
                    return True
        return False


class Literal:
    def __init__(self):
        self.id = 0
        self.value = False
        self.clauses = set()
        self.is_modifiable = True

    def remove_clause(self, clause_id):
        for clause in self.clauses:
            if clause.clause_id == clause_id:
                self.clauses.remove(clause)
            break


class SatData:
    clauses = []
    no_clauses = -1
    no_literals = -1

    def __init__(self):

        self.literals = {}
        self.read_data("../sudoku-rules.txt")
        self.read_additional_rules("../sudoku-example.txt")

    def read_data(self, path):
        file = open(path, "r")
        for line in file:
            elements = line.strip().split(' ')
            if elements[0] is 'p':
                SatData.no_literals = int(elements[2])
                SatData.no_clauses = int(elements[3])
            elif elements[0] is not 'c':
                variables = []
                clause = Clause()
                for elem in elements:
                    variable = int(elem)
                    if variable != 0:
                        literal = abs(variable)
                        variables.append(variable)

                        # check if literal is present in dictionary
                        if literal in self.literals.keys():
                            self.literals[literal].clauses.add(clause)
                        else:
                            new_literal = Literal()
                            new_literal.id = literal
                            new_literal.value = None
                            new_literal.clauses.add(clause)
                            self.literals[literal] = new_literal

                clause.variables = variables
                SatData.clauses.append(clause)

    def read_additional_rules(self, path):
        file = open(path, "r")
        for line in file:
            elements = line.strip().split(' ')
            variables = []
            clause = Clause()
            for elem in elements:
                variable = int(elem)
                if variable != 0:
                    literal = abs(variable)
                    variables.append(variable)

                    if literal in self.literals.keys():
                        self.literals[literal].clauses.add(clause)
                    else:
                        new_literal = Literal()
                        new_literal.id = literal
                        new_literal.value = True
                        new_literal.clauses.add(clause)
                        self.literals[literal] = new_literal

            clause.variables = variables
            SatData.clauses.append(clause)

    def get_modifiable_literals(self):
        modifiables = []
        for key in self.literals.keys():
            literal = self.literals[key]
            if literal.is_modifiable:
                modifiables.append(literal)
        return modifiables

    def is_sat(self):
        for clause in SatData.clauses:
            if not clause.get_value(self.literals):
                return False
        return True

    def set_literal(self, literal, value):
        key = literal.id
        self.literals[key].value = value
        self.literals[key].is_modifiable = False


class DpSatSolver:
    is_solution_found = False

    def is_tautology(self, clause):
        visited = []
        for var in clause.variables:
            negated = -var
            if negated in visited:
                return True
            visited.append(var)
        return False

    def is_unit_clause(self, clause, literals):
        counter = 0
        for var in clause.variables:
            key = abs(var)
            literal = literals[key]
            if literal.is_modifiable is True:
                counter += 1
        return counter == 1

    def remove_clause(self, clause, literals):
        for var in clause.variables:
            key = abs(var)
            literal = literals[key]
            literal.remove_clause(clause.clause_id)
            SatData.clauses.remove(clause)
            if len(literal.clauses) == 0:
                literals.pop(key)

    def handle_unit_clause(self, clause, literals):
        for var in clause.variables:
            key = abs(var)
            literal = literals[key]
            if literal.is_modifiable:
                literal.is_modifiable = False
                literal.value = True if var > 0 else False

    def is_pure(self, literal):
        appearances = len(literal.clauses)
        counter = 0
        for clause in literal.clauses:
            for var in clause.variables:
                if abs(var) == literal.id:
                    counter += 1 if var > 0 else -1
        return abs(counter) == appearances, counter > 0

    def handle_purity(self, literal, type):
        literal.is_modifiable = False
        literal.value = type

    def pre_process_clausses(self, data):
        for key in data.literals.keys():
            literal = data.literals[key]
            is_pure, type = self.is_pure(literal)
            if is_pure:
                self.handle_purity(literal, type)

        for clause in SatData.clauses:
            if self.is_tautology(clause):
                self.remove_clause(clause, data.literals)

    def simplify(self, data):
        counter = 0
        for clause in SatData.clauses:
            clause_value = clause.get_value(data.literals)
            if clause_value is False and self.is_unit_clause(clause, data.literals):
                self.handle_unit_clause(clause, data.literals)
                counter += 1
        return counter > 0

    def write_results(self, data):
        file = open("../results.txt", "w")
        line = "p cnf 81 81\n"
        file.write(line)
        for key in data.literals.keys():
            literal = data.literals[key]
            if literal.value is True:
                line = ""
                line += str(key) + " 0\n"
                file.write(line)
        file.close()

    def recursive_step_dp(self, data):

        simplify = True
        while simplify:
            simplify = self.simplify(data)

        if data.is_sat():
            self.write_results(data)
            return True

        modifiables = data.get_modifiable_literals()

        for var in modifiables:
            branch = copy.deepcopy(data)
            branch.set_literal(var, False)
            data.set_literal(var, True)

            found = self.recursive_step_dp(data)
            if found is True:
                return True
            found = self.recursive_step_dp(branch)
            if found is True:
                return True
        return False

    def DLCS(self, literal):
        positive = 0
        negative = 0

        for clause in literal.clauses:
            key = literal.id
            for elem in clause.variables:
                if abs(elem) == key:
                    if elem > 0:
                        positive += 1
                    else:
                        negative += 1

        return positive + negative, positive > negative

    def get_max_dlcs(self, modifiables):
        maxi = 0
        max_dlcs_var = None
        max_dlcs_sign = None
        for modifiable in modifiables:
            dlcs_sum, sign = self.DLCS(modifiable)
            if dlcs_sum > maxi:
                maxi = dlcs_sum
                max_dlcs_var = modifiable
                max_dlcs_sign = sign

        return max_dlcs_var, max_dlcs_sign

    def recursive_step_DLCS(self, data):
        simplify = True
        while simplify:
            simplify = self.simplify(data)

        if data.is_sat():
            self.write_results(data)
            return True

        modifiables = data.get_modifiable_literals()

        max_dlcs_var, max_dlcs_sign = self.get_max_dlcs(modifiables)

        while max_dlcs_var:
            branch = copy.deepcopy(data)
            branch.set_literal(max_dlcs_var, not max_dlcs_sign)
            data.set_literal(max_dlcs_var, max_dlcs_sign)

            found = self.recursive_step_DLCS(data)
            if found is True:
                return True
            found = self.recursive_step_DLCS(branch)
            if found is True:
                return True
            max_dlcs_var, max_dlcs_sign = self.get_max_dlcs(modifiables)
        return False

    def algorithm(self):
        data = SatData()
        self.pre_process_clausses(data)

        result = self.recursive_step_dp(data)
        if result:
            print("SAT")
        else:
            print("NON SAT")

    def algorithm_dlcs(self):
        data = SatData()
        self.pre_process_clausses(data)

        result = self.recursive_step_DLCS(data)
        if result:
            print("SAT")
        else:
            print("NON SAT")

sat = DpSatSolver()
sat.algorithm_dlcs()
