from __future__ import annotations

from pathlib import Path

import numpy as np

from vision_qa.dataset import CLASS_NAMES, IMG_SIZE, load_from_dir, load_image, split_xy


def _tf():
    import tensorflow as tf

    return tf


def build(n_classes: int = len(CLASS_NAMES)):
    tf = _tf()
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 1)),
            tf.keras.layers.Conv2D(32, 3, activation="relu"),
            tf.keras.layers.MaxPool2D(),
            tf.keras.layers.Conv2D(64, 3, activation="relu"),
            tf.keras.layers.MaxPool2D(),
            tf.keras.layers.Conv2D(128, 3, activation="relu"),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(n_classes, activation="softmax"),
        ]
    )
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model


def train(data_dir: Path, epochs: int = 8, batch_size: int = 16, out: Path | None = None):
    x, y = load_from_dir(data_dir)
    x_train, y_train, x_val, y_val = split_xy(x, y)
    model = build(y.shape[1])
    kwargs = {"epochs": epochs, "batch_size": min(batch_size, len(x_train)), "verbose": 1}
    if len(x_val):
        kwargs["validation_data"] = (x_val, y_val)
    model.fit(x_train, y_train, **kwargs)
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        model.save(out)
    return model


def load(path: Path):
    tf = _tf()
    return tf.keras.models.load_model(path)


def predict(model, image: np.ndarray) -> tuple[str, float]:
    batch = np.expand_dims(image, 0) if image.ndim == 3 else image
    probs = model.predict(batch, verbose=0)[0]
    idx = int(np.argmax(probs))
    return CLASS_NAMES[idx], float(probs[idx])


def predict_path(model, path: Path) -> tuple[str, float]:
    return predict(model, load_image(path))


def export_onnx(keras_path: Path, onnx_path: Path) -> Path:
    import tf2onnx

    tf = _tf()
    model = load(keras_path)
    spec = (tf.TensorSpec((None, IMG_SIZE, IMG_SIZE, 1), tf.float32, name="image"),)
    onnx_path.parent.mkdir(parents=True, exist_ok=True)
    tf2onnx.convert.from_keras(model, input_signature=spec, output_path=str(onnx_path))
    return onnx_path
