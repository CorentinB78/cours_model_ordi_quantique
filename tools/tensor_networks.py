import numpy as np

def merge_axes(arr, ax1, ax2):
    """
    Returns a view of the array where two adjacent axes are merged together.
    """
    if ax1 > ax2:
        return merge_axes(arr, ax2, ax1)
    if (ax1 < 0):
        raise ValueError("Axes must be >= 0")
    if (ax2 >= arr.ndim):
        raise ValueError("One of the axes is larger than the array dimension")
    if (ax2 != ax1 + 1):
        raise ValueError("ax1 and ax2 must be adjacent")
    # now we are sure that ax2 = ax1 + 1

    shape = list(arr.shape)
    arr = np.reshape(arr, shape[:ax1] + [shape[ax1] * shape[ax1 + 1]] + shape[ax1 + 2:], order='C')
    return arr


def split_axis(arr, ax, dim1, dim2):
    """
    Returns a view of the array where one axis has been split in two.
    """
    shape = list(arr.shape)
    arr = np.reshape(arr, shape[:ax] + [dim1, dim2] + shape[ax+1:], order='C', copy=False)
    return arr

######### Debug helpers #########


def check_canonicality(mps, ortho_center=None, tol=1e-10):
    """
    Check whether a given MPS is in canonical form with respect to its orthogonality center.
    """
    nb_qubits = len(mps.tensors)
    if ortho_center is None:
        ortho_center = mps.ortho_center
    out = True
    for i in range(ortho_center):
        tensor = merge_axes(mps.tensors[i], 0, 1)
        should_be_id = tensor.conj().T @ tensor
        if not np.all(np.isclose(should_be_id, np.eye(len(should_be_id)), atol=tol)):
            out = False
            print(f"Tensor at qubit {i} is not left canonical")
    for i in range(ortho_center, nb_qubits):
        tensor = merge_axes(mps.tensors[i], 1, 2)
        should_be_id = tensor @ tensor.conj().T
        if not np.all(np.isclose(should_be_id, np.eye(len(should_be_id)), atol=tol)):
            out = False
            print(f"Tensor at qubit {i} is not right canonical")

    return out