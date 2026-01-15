from math import acos, sqrt, pi
from tools.gates import INVERSE
from tools.dontread import mysterious_alpha as _mysterious_alpha


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


def shift_qubits(circuit, shift: int):
    """ Returns new circuit with qubits shifted by `shift`. """
    return [(op[0], *(qb + shift for qb in op[1:])) for op in circuit]


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


def make_circuit_ising(nb_qubits, nb_trotter=None, delta_t=0.1, J=1.0, h=0.2):
    """
    Circuit reproducing the dynamics of a 1D Ising model:

    H = J \sum Z_i Z_{i+1} + h \sum X_i

    with J = 1 and h = 0.2.
    """
    if nb_qubits <= 0:
        raise ValueError("Nb of qubits must be > 0")
    if nb_trotter is None:
        nb_trotter = nb_qubits

    circ = []

    def apply_trotter(circ, qb):
        if qb == 0:
            circ.append((('RX', delta_t * 2 * h), 0))
        else:
            circ.append(('CNOT', qb-1, qb))
            circ.append((('RZ', delta_t * 2 * J), qb))
            circ.append(('CNOT', qb-1, qb))
            circ.append((('RX', delta_t * 2 * h), qb))

    def layer_fw(circ):
        for qb in range(nb_qubits):
            apply_trotter(circ, qb)

    def layer_bw(circ):
        for qb in range(nb_qubits-1, -1, -1):
            apply_trotter(circ, qb)

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


def _make_CU_Ising(nb_qubits, nb_trotter, delta_t, J=1.0, h=0.2):
    assert nb_trotter % 2 == 0
    _nb_trotter = nb_trotter // 2
    
    def CU_Ising(x: int):
        assert x >= 1

        circ_ising = make_circuit_ising(nb_qubits, nb_trotter=x * _nb_trotter, delta_t=-delta_t, J=J, h=h)
        circ = shift_qubits(circ_ising, 1)
        
        for i in range(nb_qubits):
            circ.append(('SWAP', i, i+1))
            if i % 2 == 0:
                circ.append((('C', 'Z'), i+1, i))
            else:
                circ.append((('C', 'Y'), i+1, i))

        circ.extend(circ_ising)
            
        for i in range(nb_qubits-1, -1, -1):
            if i % 2 == 0:
                circ.append((('C', 'Z'), i+1, i))
            else:
                circ.append((('C', 'Y'), i+1, i))
            circ.append(('SWAP', i, i+1))
                
        return circ
        
    return CU_Ising


def _make_QPE_circuit(nb_result_qubits, CU_gen):
    if nb_result_qubits <= 0:
        raise ValueError("Nb of qubits must be > 0")
    out = []

    for k in range(nb_result_qubits):
        out.append(('H', k))
        
    for k in range(nb_result_qubits):
        out = out + shift_qubits(CU_gen(2**k), nb_result_qubits - 1)
        # out.append((('C', ('P', alpha * float(2**k))), nb_result_qubits - 1, nb_result_qubits))
        for i in range(nb_result_qubits - 2, k-1, -1):
            out.append(('SWAP', i, i+1))

    out = out + make_inv_QFT_circuit(nb_result_qubits)
    
    for k in range(nb_result_qubits):
        out.append(('M', k))

    return out


def make_QPE_circuit_phase(nb_result_qubits, alpha=None):
    """Circuit for Quantum Phase Estimation with U being a phase gate on a single qubit with a mysterious phase..."""
    if alpha is None:
        alpha = _mysterious_alpha
        
    circ = _make_QPE_circuit(nb_result_qubits, lambda x: [(('C', ('P', alpha * float(x))), 0, 1)])

    return circ


def make_QPE_circuit_Ising(nb_Ising_qubits, nb_result_qubits, nb_trotter, delta_t, J=1.0, h=0.2):
    """Circuit for Quantum Phase Estimation of an Ising chain Hamiltonian."""
    
    CU_Ising = _make_CU_Ising(nb_Ising_qubits, nb_trotter, delta_t, J=J, h=h)    
    circ = _make_QPE_circuit(nb_result_qubits, CU_Ising)

    return circ
