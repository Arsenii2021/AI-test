#Author: Arsenii Kostenko

from PIL import Image
import numpy as np
import os

# Папка с обучающими изображениями
image_folder = 'путь_к_папке_с_изображениями'

# Создаём пустой список для хранения массивов изображений
images_array = []

# Проход по файлам в папке с изображениями
for filename in os.listdir(image_folder):
    # Загрузка изображения с помощью Pillow
    img = Image.open(os.path.join(image_folder, filename))
    # Преобразование изображения в массив пикселей
    img_array = np.array(img)
    # Добавление массива изображения в список
    images_array.append(img_array)
