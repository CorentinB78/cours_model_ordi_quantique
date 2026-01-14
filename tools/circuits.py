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
    if nb_qubits <= 0:
        raise ValueError("Nb of qubits must be > 0")
    circuit = [('H', 0)]
    for i in range(nb_qubits - 1):
        circuit.append(('CNOT', i, i+1))

    return circuit


def make_W_circuit(nb_qubits):
    """Returns a circuit producing a W state"""
    if nb_qubits <= 0:
        raise ValueError("Nb of qubits must be > 0")
    rot = lambda n: ('RY', 2 * acos(1. / sqrt(n)))
    circ = []
    circ.append((rot(nb_qubits), 0))
    for n in range(1, nb_qubits-1):
        circ.append((('C', rot(nb_qubits - n)), n-1, n))
    for n in range(nb_qubits-1, 0, -1):
        circ.append(('CNOT', n-1, n))
    circ.append(('X', 0))
    return circ


def make_circuit_ising(nb_qubits, nb_trotter=None, delta_t=0.1):
    """
    Circuit reproducing the dynamics of a 1D Ising model:

    H = -J \sum Z_i Z_{i+1} + h \sum X_i

    with J = 1 and h = 0.2.
    """
    if nb_qubits <= 0:
        raise ValueError("Nb of qubits must be > 0")
    if nb_trotter is None:
        nb_trotter = nb_qubits
    J = 1.0
    h = 0.2
    phi = 2 * delta_t * sqrt(J**2 + h**2)
    theta = acos(2 * delta_t * J / phi)
    circ = []

    def layer_fw(circ):
        circ.append((('RX', delta_t * h), 0))
        for i in range(nb_qubits-1):
            circ.append(('CNOT', i, i+1))
            circ.append((('RY', -theta), i+1))
            circ.append((('RZ', phi), i+1))
            circ.append((('RY', theta), i+1))
            circ.append(('CNOT', i, i+1))

    def layer_bw(circ):
        for i in range(nb_qubits-2, 0, -1):
            circ.append(('CNOT', i, i+1))
            circ.append((('RY', -theta), i+1))
            circ.append((('RZ', phi), i+1))
            circ.append((('RY', theta), i+1))
            circ.append(('CNOT', i, i+1))
        circ.append((('RX', delta_t * h), 0))

    for _ in range(nb_trotter // 2):
        layer_fw(circ)
        layer_bw(circ)

    if nb_trotter % 2 == 1:
        layer_fw(circ)

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
   
