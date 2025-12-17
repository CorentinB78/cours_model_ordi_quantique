import numpy as np

GATES_1QB = {
    'M': None, # measurement
    'X': np.array([[0, 1], [1, 0]]),
    'Y': np.array([[0, -1j], [1j, 0]]),
    'Z': np.array([[1, 0], [0, -1]]),
    'H': np.array([[1, -1], [1, 1]]) / np.sqrt(2.),
    'S': np.array([[1., 0.], [0., 1j]]),
    'T': np.array([[1., 0.], [0., np.exp(1j * np.pi / 4.)]]),
}

GATES_2QB = {
    'CZ': np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]),
    'CNOT': np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]),
    'SWAP': np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]),
}
