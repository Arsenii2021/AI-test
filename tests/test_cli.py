from pathlib import Path

import pytest

from vision_qa.cli import main
from vision_qa.synth import generate


def test_cli_synth(tmp_path: Path):
    out = tmp_path / "screens"
    assert main(["synth", "--out", str(out), "--per-class", "2"]) == 0
    assert any(out.joinpath("ready").glob("*.png"))


def test_cli_infer_fails_on_mismatch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    image = generate(tmp_path / "screens", per_class=1) / "boot" / "boot_000.png"

    class Dummy:
        def predict(self, _batch, verbose=0):
            import numpy as np

            return np.array([[0.1, 0.7, 0.1, 0.1]])

    monkeypatch.setattr("vision_qa.model.load", lambda _p: Dummy())
    rc = main(["infer", str(image), "--model", str(tmp_path / "m.keras"), "--expect", "ready"])
    assert rc == 1
