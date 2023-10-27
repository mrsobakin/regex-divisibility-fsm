import sys
from greenery import fsm, lego


GRAPHVIZ_HEADER = """\
digraph finite_state_machine {
    fontname="Helvetica,Arial,sans-serif"
    node [fontname="Helvetica,Arial,sans-serif"]
    edge [fontname="Helvetica,Arial,sans-serif"]
    rankdir=LR;
    node [shape = doublecircle]; 0;
    node [shape = point]; entry;
    node [shape = circle];
    entry -> 0;"""


# transitions[curr_state][digit] = next_state
def build_transitions(base, divisor):
    transitions = {}

    for i in range(divisor):
        transitions[i] = {}

    for i in range(divisor * base):
        transitions[i // base][str(i % base)] = i % divisor

    return transitions


def print_transitions_graphviz(transitions):
    for current_state, v in transitions.items():
        for digit, next_state in v.items():
            print(f"{current_state} -> {next_state} [label = \"{digit}\"];")


def print_graphviz_dot(base, divisor):
    print(GRAPHVIZ_HEADER)

    transitions = build_transitions(base, divisor)
    print_transitions_graphviz(transitions)

    print("}")


def calc_regex(base, divisor):
    machine = fsm.fsm(
        alphabet=list(map(str, range(base))),
        states=list(range(divisor)),
        initial=0,
        finals={0},
        map=build_transitions(base, divisor)
    )

    return lego.from_fsm(machine)


if __name__ == "__main__":
    cmd = sys.argv[1]
    base, divisor = map(int, sys.argv[2:4])

    if cmd == "regex":
        print(calc_regex(base, divisor))
    elif cmd == "graphviz":
        print_graphviz_dot(base, divisor)
    else:
        print("Invalid command")
