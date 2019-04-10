from main.state import Container

states = []

sink = Container()
combinations = sink.get_all_combinations()
a = 2


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
        if state.repsects_constraints():
            valid_states.append(state)
    return valid_states


generate_states([0 for _ in range(len(combinations))], 0, 0)
valid_constraint_states = keep_valid_constraint_states(states)
print(len(valid_constraint_states))
