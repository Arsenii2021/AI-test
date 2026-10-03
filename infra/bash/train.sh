#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

python -m vision_qa synth --out data/screens --per-class "${PER_CLASS:-24}"
python -m vision_qa train --data data/screens --epochs "${EPOCHS:-8}" --model models/ui.keras
python -m vision_qa export-onnx --model models/ui.keras --onnx models/ui.onnx
