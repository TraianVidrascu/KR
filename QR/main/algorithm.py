from main.state import Container

states = []

sink = Container()
combinations = sink.get_all_combinations()


def generate_states(combination, row, column):
    if row > 4:
        print(combination)
        state = Container()
        state.set_values(combination)
        states.append(state)
        return

    if column >= len(combinations[row]):
        return

    pair = combinations[row][column]
    combination[row] = pair
    generate_states(combination[:], row + 1, column)
    generate_states(combination[:], row, column + 1)


def keep_valid_states(states):
    valid_states = []
    for state in states:
        if state.is_valid():
            valid_states.append(state)
    return valid_states


generate_states([0, 0, 0, 0, 0], 0, 0)
valid_states = keep_valid_states(states)
print(len(valid_states))
