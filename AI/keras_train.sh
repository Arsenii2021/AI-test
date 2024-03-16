#!/bin/bash

# Переменные
VENV_NAME="myenv"
DATASET_PATH="path/to/keras_dataset"
MODEL_SCRIPT="path/to/keras_model.py"
MODEL_OUTPUT="trained_model.h5"

# Активация виртуальной среды
source activate $VENV_NAME

# Загрузка датасета и обучение модели
python $MODEL_SCRIPT --dataset $DATASET_PATH --epochs 10 --batch_size 32 --output_model $MODEL_OUTPUT

# Деактивация виртуальной среды
deactivate
