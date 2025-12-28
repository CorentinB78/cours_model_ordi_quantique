from math import acos, sqrt

def make_GHZ_circuit(nb_qubits):
    """Returns a circuit producing a GHZ state"""
    circuit = [('H', 0)]
    for i in range(nb_qubits - 1):
        circuit.append(('CNOT', i, i+1))

    return circuit


def make_W_circuit(nb_qubits):
    """Returns a circuit producing a W state"""
    rot = lambda n: ('RY', 2 * acos(1. / sqrt(n)))
    circ = []
    circ.append((rot(nb_qubits), 0))
    for n in range(1, nb_qubits-1):
        circ.append((('C', rot(nb_qubits - n)), n-1, n))
    for n in range(nb_qubits-1, 0, -1):
        circ.append(('CNOT', n-1, n))
    circ.append(('X', 0))
    return circ

####### Circuits utils #########

def get_nb_qubits(circuit):
    """Returns the number of qubits involved in the circuit"""
    n = 0
    for op in circuit:
        for i in op[1:]:
            n = max(n, i + 1)
    return n

