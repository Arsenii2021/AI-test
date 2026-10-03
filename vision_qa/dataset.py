from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

IMG_SIZE = 128
CLASS_NAMES = ("boot", "login", "ready", "error")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp"}


def class_index(name: str) -> int:
    try:
        return CLASS_NAMES.index(name)
    except ValueError as exc:
        raise ValueError(f"unknown class {name!r}, expected {CLASS_NAMES}") from exc


def one_hot(name: str) -> np.ndarray:
    y = np.zeros(len(CLASS_NAMES), dtype=np.float32)
    y[class_index(name)] = 1.0
    return y


def load_image(path: Path, size: int = IMG_SIZE) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(path)
    image = cv2.resize(image, (size, size), interpolation=cv2.INTER_AREA)
    return (image.astype(np.float32) / 255.0)[..., np.newaxis]


def load_from_dir(root: Path, size: int = IMG_SIZE) -> tuple[np.ndarray, np.ndarray]:
    xs: list[np.ndarray] = []
    ys: list[np.ndarray] = []
    for name in CLASS_NAMES:
        folder = root / name
        if not folder.is_dir():
            continue
        for path in sorted(folder.iterdir()):
            if path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            xs.append(load_image(path, size))
            ys.append(one_hot(name))
    if not xs:
        raise FileNotFoundError(f"no labeled images under {root}")
    return np.stack(xs), np.stack(ys)


def split_xy(
    x: np.ndarray,
    y: np.ndarray,
    val_ratio: float = 0.2,
    seed: int = 7,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(x))
    n_val = max(1, int(len(x) * val_ratio)) if len(x) > 1 else 0
    val_idx, train_idx = idx[:n_val], idx[n_val:]
    if len(train_idx) == 0:
        train_idx = val_idx
        val_idx = np.array([], dtype=int)
        return x[train_idx], y[train_idx], x[train_idx][:0], y[train_idx][:0]
    return x[train_idx], y[train_idx], x[val_idx], y[val_idx]
