from itertools import product

import pytest
import torch
from torch_cluster import nearest

from .utils import tensor, grad_dtypes

devices = [torch.device('cuda')]


@pytest.mark.skipif(not torch.cuda.is_available(), reason='CUDA not available')
@pytest.mark.parametrize('dtype,device', product(grad_dtypes, devices))
def test_nearest(dtype, device):
    x = tensor([
        [-1, -1],
        [-1, +1],
        [+1, +1],
        [+1, -1],
        [-2, -2],
        [-2, +2],
        [+2, +2],
        [+2, -2],
    ], dtype, device)
    y = tensor([
        [-1, 0],
        [+1, 0],
        [-2, 0],
        [+2, 0],
    ], dtype, device)

    batch_x = tensor([0, 0, 0, 0, 1, 1, 1, 1], torch.long, device)
    batch_y = tensor([0, 0, 1, 1], torch.long, device)

    dist, idx = nearest(x, y, batch_x, batch_y)
    assert dist.tolist() == [1, 1, 1, 1, 2, 2, 2, 2]
    assert idx.tolist() == [0, 0, 1, 1, 2, 2, 3, 3]