import numpy as np
from .circuits import get_nb_qubits

def print_state(state, ignore_zeros=True):
    """Prints amplitudes of a given state."""
    d = len(state)
    N = np.log2(d)
    for i, amp in enumerate(state):
        if (not ignore_zeros) or (abs(amp) > 1e-14):
            print(f'|{bin(i + d)[3:]}> {amp}')
    print()


def print_circuit(circuit):
    """Prints a circuit in text format. This uses unicode characters. Experimental."""
    n = get_nb_qubits(circuit)
    to_print = ""
    for qb in range(n):
        to_print += '|0>'
        for op in circuit:
            
            if len(op) == 2:
                gate, i = op
                if i != qb:
                    to_print += '\u2500\u2500\u2500' # ---
                    continue
                to_print += f'\u2500{gate[0]}\u2500' # -H-
            elif len(op) == 3:
                gate, i, j = op
                if qb < min(i, j) or max(i, j) < qb:
                    to_print += '\u2500\u2500\u2500' # ---
                    continue
                if qb == i:
                    if gate[0] == 'C':
                        to_print += '\u2500\u25cf\u2500' # -@-
                    elif gate == 'SWAP':
                        to_print += '\u2500\u00d7\u2500' # -x-
                    else:
                        raise ValueError(f"Gate '{gate}' unknown.")
                elif qb == j:
                    if gate == 'CZ':
                        to_print += '\u2500\u25cf\u2500' # -@-
                    elif gate == 'CNOT':
                        to_print += '\u2500X\u2500' # -X-
                    elif gate == 'SWAP':
                        to_print += '\u2500\u00d7\u2500' # -x-
                    elif gate[0] == 'C':
                        to_print += f'\u2500{gate[1][0]}\u2500' # -H-
                    else:
                        raise ValueError(f"Gate '{gate}' unknown.")
                else: # i < qb < j
                    to_print += '\u2500\u253c\u2500' # -|-
        to_print += "\n"

    print(to_print)
