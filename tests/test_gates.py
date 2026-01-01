import numpy as np
from numpy import testing
from tools.gates import GATES_1QB, GATES_2QB, INVERSE

def test_inverse():
    assert INVERSE['X'] == 'X'
    assert INVERSE[('RX', 0.5)] == ('RX', -0.5)
    assert INVERSE['RX', 0.5] == ('RX', -0.5)
    assert INVERSE[('C', ('P', 0.5))] == ('C', ('P', -0.5))

def test_inverse_1qb():
    angle = 1.234
    for gate in ['X', 'Y', 'Z', 'H', 'S', 'T', ('RX', angle), ('RY', angle), ('RZ', angle), ('P', angle)]:
        testing.assert_allclose(GATES_1QB[gate] @ GATES_1QB[INVERSE[gate]], np.eye(2), atol=1e-15)
  
def test_inverse_2qb():
    angle = 1.234
    for gate in ['CNOT', 'CZ', 'SWAP', ('C', 'S'), ('C', ('P', angle))]:
        testing.assert_allclose(GATES_2QB[gate] @ GATES_2QB[INVERSE[gate]], np.eye(4), atol=1e-15)