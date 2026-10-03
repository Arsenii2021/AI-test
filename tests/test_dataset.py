from pathlib import Path

import numpy as np
import pytest

from vision_qa.dataset import CLASS_NAMES, class_index, load_from_dir, one_hot, split_xy
from vision_qa.synth import generate


def test_one_hot_covers_all_classes():
    matrix = np.stack([one_hot(name) for name in CLASS_NAMES])
    assert matrix.shape == (4, 4)
    assert np.allclose(matrix.sum(axis=1), 1)
    assert class_index("error") == 3


def test_unknown_class_is_rejected():
    with pytest.raises(ValueError):
        class_index("panic")


def test_synth_dataset_roundtrip(tmp_path: Path):
    root = generate(tmp_path / "screens", per_class=3, seed=1)
    x, y = load_from_dir(root)
    assert x.shape[0] == 12
    assert x.shape[1:] == (128, 128, 1)
    assert y.shape == (12, 4)
    assert x.min() >= 0 and x.max() <= 1
    x_tr, y_tr, x_val, y_val = split_xy(x, y, val_ratio=0.25, seed=0)
    assert len(x_tr) + len(x_val) == 12
    assert len(y_tr) == len(x_tr)
