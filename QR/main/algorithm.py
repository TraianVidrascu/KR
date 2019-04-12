from graphviz import Digraph
from main.state import Container, INFLOW
from main.utils import DerivativeRules, MagnitudeRules, Magnitude, Derivative, InflowBehaviour, Names, ValueType

states = []

sink = Container()
combinations = sink.get_all_combinations()


def generate_states(combination, row, column):
    if row > 4:
        state = Container()
        state.set_values(combination)
        states.append(state)
        return

    if column >= len(combinations[row]):
        return

    pair = combinations[row][column]
    combination[row] = pair
    generate_states(combination[:], row + 1, 0)
    generate_states(combination[:], row, column + 1)


def keep_valid_constraint_states(states):
    valid_states = []
    for state in states:
        if state.repsects_constraints() and state.has_valid_values():
            valid_states.append(state)
    return valid_states


def keep_valid_relations(states):
    valid_states = []
    for state in states:
        if state.respect_relations():
            valid_states.append(state)
    return valid_states


def is_transition(first, second):
    first_quantities = first.quantities
    second_quantities = second.quantities
    ok = 0
    for i in range(len(first_quantities)):
        f = first_quantities[i]
        s = second_quantities[i]
        if f.derivative is Derivative.POSITIVE and f.magnitude is Magnitude.ZERO:
            ok = 1
        if s.derivative is Derivative.ZERO and s.magnitude is Magnitude.POSITIVE:
            ok += 1
        if ok == 8:
            pass

    fast_changes = 0
    slow_changes = 0

    is_inflow_derivative_changed = False
    is_magnitude_changed = False
    is_derivative_changed = False
    for i in range(0, len(first_quantities)):
        first_derivative = first_quantities[i].derivative
        first_magnitude = first_quantities[i].magnitude

        second_derivative = second_quantities[i].derivative
        second_magnitude = second_quantities[i].magnitude

        if first_derivative is not second_derivative:
            is_derivative_changed = True
            if first_quantities[i].name is INFLOW:
                is_inflow_derivative_changed = True

        if first_magnitude is not second_magnitude:
            is_magnitude_changed = True

        # checks if longer changes take place as fast as instant changes
        if first_magnitude in ValueType.POINTS and second_magnitude in ValueType.INTERVALS:
            fast_changes += 1
        if first_derivative in ValueType.POINTS and second_derivative in ValueType.INTERVALS:
            fast_changes += 1

        if first_magnitude not in ValueType.POINTS and second_magnitude is not first_magnitude:
            slow_changes += 1
        if first_derivative not in ValueType.POINTS and second_derivative is not first_derivative:
            slow_changes += 1

        if fast_changes > 0 and slow_changes > 0:
            return False

        # derivative rules
        derivate_rule_space = DerivativeRules.derivative_rules[first_derivative]
        possible_magnitude_derivative_values = derivate_rule_space[first_magnitude]
        is_possible = False
        for possible_magnitude, possible_derivative in possible_magnitude_derivative_values:
            if possible_magnitude is second_magnitude and possible_derivative is second_derivative:
                is_possible = True
        if not is_possible:
            return False

        # checking magnitude rules
        value_space_rules = MagnitudeRules.magnitude_rules[first_magnitude]
        if second_magnitude not in value_space_rules[first_derivative]:
            return False

        # inflow behaviour rules
        if first_quantities[i].name is INFLOW:
            inflow_rule = InflowBehaviour.inflow_behaviour[first_derivative]
            possible_magnitude_derivative_values = inflow_rule[first_magnitude]
            is_possible = False
            for possible_magnitude, possible_derivative in possible_magnitude_derivative_values:
                if second_magnitude is possible_magnitude and second_derivative is possible_derivative:
                    is_possible = True
            if not is_possible:
                return False

    if not is_inflow_derivative_changed and not is_magnitude_changed and is_derivative_changed:
        return False
    return True


def get_transitions(states):
    transitions = {}
    for i in range(0, len(states)):
        transitions[str(i)] = []
        for j in range(0, len(states)):
            if i != j:
                first = states[i]
                second = states[j]
                if is_transition(first, second):
                    transitions[str(i)].append(str(j))
    return transitions


def get_initial_node(states):
    node = 0
    for state in states:
        quantities = state.quantities
        is_initial = True
        for quantity in quantities:

            if quantity.magnitude is not Magnitude.ZERO:
                is_initial = False
            if quantity.name is not INFLOW and quantity.derivative is not Derivative.ZERO:
                is_initial = False
            if quantity.name is INFLOW and quantity.derivative is not Derivative.POSITIVE:
                is_initial = False
        if is_initial:
            return str(node)
        node += 1
    return None


def create_graph_nodes(good_states, keep_states):
    graph = Digraph(format='png')
    idx = 0
    count = 0
    labels_values = dict()
    for state in good_states:
        if keep_states[idx]:
            count += 1
            quantities = state.quantities
            label = str(state.name) + "\n"
            for quantity in quantities:
                mag = quantity.magnitude
                dev = quantity.derivative
                label += quantity.name + "(" + Names.magnitude_names[mag] + ", " + Names.derivative_names[dev] + ")\n"
                labels_values[idx] = label
            graph.node(str(idx), label)
        idx += 1
    print(count)
    return graph


def create_graph_edges(states, t):
    for idx in range(len(states)):
        for out in t[str(idx)]:
            graph.edge(str(idx), out)


def filter_transition(node, vis, t, nt):
    out_bounds = t[node]
    vis[node] = True
    for out_bound in out_bounds:
        nt[node].append(out_bound)
        if out_bound not in vis.keys() or vis[out_bound] is False:
            filter_transition(out_bound, vis, t, nt)


def filter_states(valid_constraints_relations, transitions):
    keep_states = [False for _ in range(len(valid_constraints_relations))]
    for key in transitions.keys():
        for out in transitions[key]:
            keep_states[int(out)] = True
            keep_states[int(key)] = True

    return keep_states


def name_states(node, valid_constraints_relations, new_transitions):
    key = int(node)
    current_state = valid_constraints_relations[key]
    current_state.name = str(Container.NAME)
    out_bounds = new_transitions[node]

    stack = out_bounds[:]
    while len(stack) > 0:
        front = stack[0]
        stack.remove(front)
        child_state = valid_constraints_relations[int(front)]
        if child_state.name == "":
            Container.NAME += 1
            child_state.name = str(Container.NAME)
            children = new_transitions[front]
            for child in children:
                new_child_state = valid_constraints_relations[int(child)]
                if new_child_state.name == "":
                    stack.append(child)


generate_states([0 for _ in range(len(combinations))], 0, 0)
valid_constraint_states = keep_valid_constraint_states(states)
valid_constraints_relations = keep_valid_relations(valid_constraint_states)

transitions = get_transitions(valid_constraints_relations)
initial_node = get_initial_node(valid_constraints_relations)

new_transitions = {}
for key in transitions.keys():
    new_transitions[key] = []
filter_transition(initial_node, {}, transitions, new_transitions)

keep = filter_states(valid_constraints_relations, new_transitions)

name_states(initial_node, valid_constraints_relations, new_transitions)
graph = create_graph_nodes(valid_constraints_relations, keep)
create_graph_edges(valid_constraints_relations, new_transitions)

graph.render('../states', view=True)
