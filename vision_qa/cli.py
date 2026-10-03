from __future__ import annotations

import argparse
from pathlib import Path

from vision_qa.dataset import CLASS_NAMES


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--model", type=Path, default=Path("models/ui.keras"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vision-qa")
    sub = parser.add_subparsers(dest="cmd", required=True)

    synth = sub.add_parser("synth", help="generate synthetic console screenshots")
    synth.add_argument("--out", type=Path, default=Path("data/screens"))
    synth.add_argument("--per-class", type=int, default=24)

    train = sub.add_parser("train")
    train.add_argument("--data", type=Path, default=Path("data/screens"))
    train.add_argument("--epochs", type=int, default=8)
    train.add_argument("--batch-size", type=int, default=16)
    _add_common(train)

    infer = sub.add_parser("infer")
    infer.add_argument("image", type=Path)
    _add_common(infer)
    infer.add_argument("--expect", choices=CLASS_NAMES)

    export = sub.add_parser("export-onnx")
    _add_common(export)
    export.add_argument("--onnx", type=Path, default=Path("models/ui.onnx"))

    cap = sub.add_parser("capture")
    src = cap.add_mutually_exclusive_group(required=True)
    src.add_argument("--url")
    src.add_argument("--domain")
    cap.add_argument("--out", type=Path, default=Path("data/capture.png"))

    args = parser.parse_args(argv)

    if args.cmd == "synth":
        from vision_qa.synth import generate

        generate(args.out, per_class=args.per_class)
        print(args.out)
        return 0

    if args.cmd == "train":
        from vision_qa.model import train as fit

        fit(args.data, epochs=args.epochs, batch_size=args.batch_size, out=args.model)
        print(args.model)
        return 0

    if args.cmd == "infer":
        from vision_qa.model import load, predict_path

        label, conf = predict_path(load(args.model), args.image)
        print(f"{label}\t{conf:.4f}")
        if args.expect and label != args.expect:
            return 1
        return 0

    if args.cmd == "export-onnx":
        from vision_qa.model import export_onnx

        print(export_onnx(args.model, args.onnx))
        return 0

    if args.cmd == "capture":
        from vision_qa.capture import capture_domain, capture_url

        path = capture_url(args.url, args.out) if args.url else capture_domain(args.domain, args.out)
        print(path)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
