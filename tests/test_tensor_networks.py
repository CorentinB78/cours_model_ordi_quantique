import pytest
import numpy as np
from tools.tensor_networks import merge_axes

@pytest.mark.parametrize("ax1, ax2, expected_shape",
                         [(0, 1, (2, 3, 4)),
                          (1, 0, (2, 3, 4)),
                          (1, 2, (1, 6, 4)),
                          (2, 1, (1, 6, 4)),
                          (2, 3, (1, 2, 12)),
                         ])
def test_merge_axes(ax1, ax2, expected_shape):
    a = np.empty((1, 2, 3, 4))
    a = merge_axes(a, ax1, ax2)
    assert a.shape == expected_shape
