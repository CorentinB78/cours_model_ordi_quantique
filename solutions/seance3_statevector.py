import numpy as np
from tools.gates import GATES_1QB, GATES_2QB

def apply_1qb_gate(state, gate, qubit, nb_qubits):
    assert 0 <= qubit < nb_qubits
    unitary = GATES_1QB[gate]
    if qubit > 0:
        unitary = np.kron(np.eye(2**qubit), unitary)
    if qubit < nb_qubits - 1:
        unitary = np.kron(unitary, np.eye(2**(nb_qubits - qubit - 1)))

    return unitary @ state

def apply_adj_2qb_gate(state, gate, qubit1, qubit2, nb_qubits):
    assert qubit1 != qubit2
    assert 0 <= qubit1 < nb_qubits
    assert 0 <= qubit2 < nb_qubits
    assert abs(qubit1 - qubit2) == 1

    unitary = GATES_2QB[gate]
    swap = GATES_2QB['SWAP']
    if qubit1 > qubit2:
        unitary = swap @ unitary @ swap
        qubit1, qubit2 = qubit2, qubit1

    # now we have qubit1 < qubit2
    
    if qubit1 > 0:
        unitary = np.kron(np.eye(2**qubit1), unitary)
    if qubit2 < nb_qubits - 1:
        unitary = np.kron(unitary, np.eye(2**(nb_qubits - qubit2 - 1)))

    return unitary @ state

def apply_measure(state, qubit, nb_qubits):
    proj_0 = np.array([[1, 0], [0, 0]])
    if qubit > 0:
        proj_0 = np.kron(np.eye(2**qubit), proj_0)
    if qubit < nb_qubits - 1:
        proj_0 = np.kron(proj_0, np.eye(2**(nb_qubits - qubit - 1)))

    state_0 = proj_0 @ state
    norm_0 = np.linalg.norm(state_0)
    prob_0 = norm_0**2

    if np.random.uniform(0., 1.) < prob_0:
        return state_0 / norm_0, 0
    else:
        state_1 = state - state_0
        return state_1 / np.linalg.norm(state_1), 1


def emulate_circuit(circuit, nb_qubits):
    psi = np.zeros((2 ** nb_qubits,), dtype=complex)
    psi[0] = 1.

    for op in circuit:
        if len(op) == 2:
            gate, qb = op
            psi = apply_1qb_gate(psi, gate, qb, nb_qubits)
        elif len(op) == 3:
            gate, qb1, qb2 = op
            psi = apply_adj_2qb_gate(psi, gate, qb1, qb2, nb_qubits)

    return psi

if __name__ == '__main__':
    from tools.circuits import make_GHZ_circuit
    from tools.display import print_state
    
    circuit_GHZ = make_GHZ_circuit(4)
    
    psi = emulate_circuit(circuit_GHZ, 4)
    print_state(psi)
    print(np.linalg.norm(psi))