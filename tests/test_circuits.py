import numpy as np
from tools.circuits import make_circuit_ising
from solutions.seance3_statevector import emulate_circuit
from scipy import linalg
from tools.gates import PAULIS


def test_circuit_ising():
    J = 0.3
    h = 1.7
    circ = make_circuit_ising(2, 100, delta_t=0.01, J=J, h=h)
    psi, _ = emulate_circuit(circ, 2)
    
    amp = linalg.expm(-1.0j * (J * np.diag([1, -1, -1, 1]) + h * np.kron(PAULIS['X'], np.eye(2)) + h * np.kron(np.eye(2), PAULIS['X'])) * 1.0)[0, 0]
    
    assert np.abs(psi[0] - amp) < 1e-4