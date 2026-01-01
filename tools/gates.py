import numpy as np
from math import cos, sin, pi

class _GateDict():

    def __init__(self, dictionary):
        self._dict = dictionary

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._dict[key]
        else:
            gate_name = key[0]
            args = key[1:]
            return self._dict[gate_name](*args)

    def __setitem__(self, key, value):
        if key in self.available_gates:
            raise ValueError(f"Gate '{key}' already exists. Find another name.")
        self._dict[key] = value

    @property
    def available_gates(self):
        return self._dict.keys()

######## Predefined gates ########

PAULIS = {
    'I': np.eye(2),
    'X': np.array([[0, 1], [1, 0]]),
    'Y': np.array([[0, -1j], [1j, 0]]),
    'Z': np.array([[1, 0], [0, -1]]),
}

_GATES_1QB = {
    'M': None, # measurement
    'X': PAULIS['X'],
    'Y': PAULIS['Y'],
    'Z': PAULIS['Z'],
    'H': np.array([[1, 1], [1, -1]]) / np.sqrt(2.),
    'S': np.array([[1., 0.], [0., 1j]]),
    'T': np.array([[1., 0.], [0., np.exp(1j * pi / 4.)]]),
    'RX': lambda theta: cos(0.5 * theta) * np.eye(2) - 1j * sin(0.5 * theta) * PAULIS['X'],
    'RY': lambda theta: cos(0.5 * theta) * np.eye(2) - 1j * sin(0.5 * theta) * PAULIS['Y'],
    'RZ': lambda theta: cos(0.5 * theta) * np.eye(2) - 1j * sin(0.5 * theta) * PAULIS['Z'],
    'P': lambda alpha: np.array([[1., 0.], [0., np.exp(1j * alpha)]]),
}

_GATES_2QB = {
    'CZ': np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]),
    'CNOT': np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]),
    'SWAP': np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]),
    'C': lambda gate: np.block([[np.eye(2), np.zeros((2, 2))], [np.zeros((2, 2)), GATES_1QB[gate]]]),
}

GATES_1QB = _GateDict(_GATES_1QB)
GATES_2QB = _GateDict(_GATES_2QB)

######## Inverses ###########

_INVERSE = {
    'X': 'X',
    'Y': 'Y',
    'Z': 'Z',
    'H': 'H',
    'S': ('P', -0.5*pi),
    'T': ('P', -0.25*pi),
    'RX': lambda theta: ('RX', -theta),
    'RY': lambda theta: ('RY', -theta),
    'RZ': lambda theta: ('RZ', -theta),
    'P': lambda alpha: ('P', -alpha),

    'CZ': 'CZ',
    'CNOT': 'CNOT',
    'SWAP': 'SWAP',
}

INVERSE = _GateDict(_INVERSE)

INVERSE['C'] = lambda gate: ('C', INVERSE[gate])
