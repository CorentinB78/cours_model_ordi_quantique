
def make_GHZ_circuit(nb_qubits):
    """Returns a circuit producing a GHZ state"""
    circuit = [('H', 0)]
    for i in range(nb_qubits - 1):
        circuit.append(('CNOT', i, i+1))

    return circuit

####### Circuits utils #########

def get_nb_qubits(circuit):
    """Returns the number of qubits involved in the circuit"""
    n = 0
    for op in circuit:
        for i in op[1:]:
            n = max(n, i + 1)
    return n

