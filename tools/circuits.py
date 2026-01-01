from math import acos, sqrt, pi
from tools.gates import INVERSE
 
####### Circuits utils #########

def get_nb_qubits(circuit):
    """Returns the number of qubits involved in the circuit"""
    n = 0
    for op in circuit:
        for i in op[1:]:
            n = max(n, i + 1)
    return n

def invert_circuit(circuit):
    """Invert a circuit"""
    out = []
    for op in circuit[::-1]:
        out.append((INVERSE[op[0]], *op[1:]))

    return out

######## Useful circuits #########

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

def make_QFT_circuit(nb_qubits):
    """QFT circuit without swap part"""
    if nb_qubits <= 0:
        raise ValueError("Nb of qubits must be > 0")
    out = []

    def phase_gate(k):
        return ('P', pi / 2**(k-1))

    for i in range(nb_qubits-1):
        out.append(('H', i))
        gate = ('C', phase_gate(2))
        out.append((gate, i + 1, i))
        for k in range(3, nb_qubits - i + 1):
            out.append(('SWAP', i + k - 2, i + k - 3))
            gate = ('C', phase_gate(k))
            out.append((gate, i + k - 1, i + k - 2))

        for k in range(nb_qubits-2, i, -1):
            out.append(('SWAP', k, k-1))

    out.append(('H', nb_qubits-1))
    return out

def make_inv_QFT_circuit(nb_qubits):
    """Inverse QFT circuit without swap part"""
    return invert_circuit(make_QFT_circuit(nb_qubits))
   
