import copy

import sys


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

    def __init__(self, filepath):
        self.reset_clauses()
        self.literals = {}
        self.read_data("sudoku-rules.txt")
        self.read_additional_rules(filepath)

    def reset_clauses(self):
        SatData.clauses = []
        SatData.no_clauses = -1
        SatData.no_literals = -1


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

    def __init__(self, filepath):
        self.is_solved = False
        self.filepath = filepath
        self.splits = 0

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
        file_name = self.filepath.split('.')[0]
        file = open(file_name + ".out", "w")
        literals_no = len(data.literals.keys())
        line = "p cnf " + str(literals_no) + " " + str(literals_no) + "\n"
        file.write(line)
        for key in data.literals.keys():
            literal = data.literals[key]
            line = ""
            if literal.value is True:
                line += str(key) + " 0\n"
            else:
                line += "-" + str(key) + " 0\n"
            file.write(line)
        file.close()

    def write_negative_results(self):
        file_name = self.filepath.split('.')[0]
        file = open(file_name + ".out", "w")
        file.write("")

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

            self.splits += 1

            found = self.recursive_step_dp(data)
            if found is True:
                return True
            found = self.recursive_step_dp(branch)
            if found is True:
                return True
        return False

    def algorithm(self):
        self.is_solved = False
        self.splits = 0
        data = SatData(self.filepath)
        self.pre_process_clausses(data)

        result = self.recursive_step_dp(data)
        if result:
            self.is_solved = True
            print("SAT")
        else:
            self.write_negative_results()
            print("NON SAT")

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

            self.splits += 1

            found = self.recursive_step_DLCS(data)
            if found is True:
                return True
            found = self.recursive_step_DLCS(branch)
            if found is True:
                return True
            modifiables = data.get_modifiable_literals()
            max_dlcs_var, max_dlcs_sign = self.get_max_dlcs(modifiables)
        return False

    def algorithm_dlcs(self):
        self.is_solved = False
        self.splits = 0
        data = SatData(self.filepath)
        self.pre_process_clausses(data)

        result = self.recursive_step_DLCS(data)
        if result:
            self.is_solved = True
            print("SAT")
        else:
            self.write_negative_results()
            print("NON SAT")

    def get_clause_size(self, clause, literals):
        counter = 0
        for var in clause.variables:
            key = abs(var)
            literal = literals[key]
            if literal.is_modifiable is True:
                counter += 1
        return counter

    def get_smallest_size(self, data):
        mini = 100000000
        for clause in data.clauses:
            value = clause.get_value(data.literals)
            if not value:
                length = self.get_clause_size(clause, data.literals)
                if length < mini:
                    mini = length
        return mini

    def MOMs_heuristic(self, literal, data, smallest_size):
        positive = 0
        negative = 0
        k = 2
        for clause in literal.clauses:
            length = self.get_clause_size(clause, data.literals)
            value = clause.get_value(data.literals)
            if length == smallest_size and not value:
                for var in clause.variables:
                    if abs(var) == literal.id:
                        if var > 0:
                            positive += 1
                        else:
                            negative += 1
        return (positive + negative) * (2 ** k) + positive * negative

    def get_max_MOMs(self, modifiables, data):
        maxi = -1
        smallest_size = self.get_smallest_size(data)
        max_MOMs_var = None
        for modifiable in modifiables:
            MOMs_value = self.MOMs_heuristic(modifiable, data, smallest_size)
            if MOMs_value > maxi:
                maxi = MOMs_value
                max_MOMs_var = modifiable
        return max_MOMs_var

    def recursive_step_MOMs(self, data):

        simplify = True
        while simplify:
            simplify = self.simplify(data)

        if data.is_sat():
            self.write_results(data)
            return True

        modifiables = data.get_modifiable_literals()
        max_moms = self.get_max_MOMs(modifiables, data)

        while max_moms:
            branch = copy.deepcopy(data)
            branch.set_literal(max_moms, False)
            data.set_literal(max_moms, True)

            self.splits += 1

            found = self.recursive_step_MOMs(data)
            if found is True:
                return True
            found = self.recursive_step_MOMs(branch)
            if found is True:
                return True

            modifiables = data.get_modifiable_literals()
            max_moms = self.get_max_MOMs(modifiables, data)

        return False

    def algorithm_MOMS(self):
        self.is_solved = False
        self.splits = 0
        data = SatData(self.filepath)
        self.pre_process_clausses(data)

        result = self.recursive_step_MOMs(data)
        if result:
            self.is_solved = True
            print("SAT")
        else:
            self.write_negative_results()
            print("NON SAT")


def run_exp(literals, sudoku_id):
    filepath = "sudoku-example.txt"

    file = open(filepath, "w")
    for literal in literals:
        line = str(literal) + " 0\n"
        file.write(line)
    file.close()

    solver = DpSatSolver(filepath)
    solver.algorithm()
    splits = solver.splits
    result = solver.is_solved
    write_exp_res("-S1", sudoku_id, splits, result)

    solver.algorithm_dlcs()
    splits = solver.splits
    result = solver.is_solved
    write_exp_res("-S2", sudoku_id, splits, result)

    solver.algorithm_MOMS()
    result = solver.is_solved
    splits = solver.splits
    write_exp_res("-S3", sudoku_id, splits, result)



def write_exp_res(alg_id, sudoku, splits, result):
    results_path = "results/results.txt"
    file = open(results_path, "a")
    line = str(sudoku) + " " + alg_id + " " + str(splits) + " " + str(result) + "\n"
    file.write(line)
    file.close()

def run_alg(literals, sudoku_id):
    if len(sys.argv) != 3:
        print("Wrong number of arguments")
    else:

        alg_id = sys.argv[1]
        filepath = sys.argv[2]

        file = open(filepath, "w")
        for literal in literals:
            line = str(literal) + " 0\n"
            file.write(line)

        solver = DpSatSolver(filepath)
        if alg_id == "-S1":
            solver.algorithm()
        elif alg_id == "-S2":
            solver.algorithm_dlcs()
        elif alg_id == "-S3":
            solver.algorithm_MOMS()

        splits = solver.splits
        result = solver.is_solved

        results_path = "results/results.txt"
        file = open(results_path, "a")
        line = sudoku_id + " " + alg_id + " " + str(splits) + " " + str(result) + "\n"
        file.write(line)


def read_sudoku_line(line):
    position = 0
    variables = []
    for row in range(1, 10):
        for column in range(1, 10):
            value = line[position]
            if value is not '.':
                number = int(value)
                var = 100 * row + 10 * column + number
                variables.append(var)
            position += 1
    return variables


def run_experiment(begin, end):
    file = open("1000 sudokus.txt", "r")
    counter = 1
    end = min(1000, end)
    while counter <= end:
        line = file.readline()
        if counter >= begin:
            literals = read_sudoku_line(line)
            run_exp(literals, counter)
        counter += 1


run_experiment(1, 49)
