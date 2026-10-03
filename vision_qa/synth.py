from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from vision_qa.dataset import CLASS_NAMES, IMG_SIZE

_PATTERNS = {
    "boot": ((20, 20, 20), "BOOT"),
    "login": ((40, 40, 90), "LOGIN"),
    "ready": ((20, 90, 40), "READY"),
    "error": ((90, 20, 20), "ERROR"),
}


def _frame(label: str, noise: float, rng: np.random.Generator) -> np.ndarray:
    color, text = _PATTERNS[label]
    img = np.full((IMG_SIZE, IMG_SIZE, 3), color, dtype=np.uint8)
    jitter = rng.integers(-12, 13, size=img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + jitter, 0, 255).astype(np.uint8)
    cv2.putText(img, text, (18, 72), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (240, 240, 240), 2, cv2.LINE_AA)
    if noise:
        grain = rng.normal(0, noise, img.shape)
        img = np.clip(img.astype(np.float32) + grain, 0, 255).astype(np.uint8)
    return img


def generate(root: Path, per_class: int = 24, seed: int = 7) -> Path:
    rng = np.random.default_rng(seed)
    for name in CLASS_NAMES:
        folder = root / name
        folder.mkdir(parents=True, exist_ok=True)
        for i in range(per_class):
            path = folder / f"{name}_{i:03d}.png"
            cv2.imwrite(str(path), _frame(name, noise=8.0, rng=rng))
    return root
