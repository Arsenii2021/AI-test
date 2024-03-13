#Author: Arsenii Kostenko
#This code testing your web through computer vision

import os
import shutil
import logging
import tensorflow as tf
from selenium import webdriver

# Настройка логирования
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

# Запрос адреса сайта и текста для поиска
site_url = input("Введите адрес сайта: ")
search_text = input("Введите текст для поиска: ")

# Логирование введенных данных
logging.debug("Адрес сайта: %s", site_url)
logging.debug("Текст для поиска: %s", search_text)

try:
    # Создание экземпляра веб-драйвера
    driver = webdriver.Chrome()

    # Логирование старта браузера
    logging.debug("Запуск браузера")

    # Открытие браузера по указанной ссылке
    driver.get(site_url)

    # Создание папки "images" на рабочем столе, если она не существует
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    images_folder = os.path.join(desktop_path, "images")
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
        logging.debug("Создана папка 'images' на рабочем столе")

    # Создание скриншота веб-страницы
    screenshot_path = os.path.join(images_folder, "screenshot.png")
    driver.save_screenshot(screenshot_path)
    logging.debug("Скриншот сохранен в папке 'images' на рабочем столе")

    # Загрузка предварительно обученной модели распознавания текста
    model = tf.keras.models.load_model('my_model.keras')

    # Логирование загрузки модели
    logging.debug("Загрузка модели распознавания текста")

   # Загрузка скриншота и предобработка изображения
    image = tf.keras.preprocessing.image.load_img(screenshot_path, target_size=(28, 28))
    image_array = tf.keras.preprocessing.image.img_to_array(image)[:,:,0]
    image_array = tf.expand_dims(image_array, 0)
    processed_image = image_array / 255.0
    # Получение предсказания модели
    predictions = model.predict(processed_image)
    predicted_label = predictions[0][0]

    # Логгирование предсказанной метки
    logging.debug("Предсказанная метка: %s", predicted_label)

    # Проверка, содержит ли предсказанный текст искомую надпись
    if search_text == predicted_label:
        print("Надпись найдена на веб-странице")
        logging.info("Надпись найдена на веб-странице")
    else:
        print("Надпись не найдена на веб-странице")
        logging.info("Надпись не найдена на веб-странице")

finally:
    # Закрытие браузера
    driver.quit()

    # Удаление папки "images"
    shutil.rmtree(images_folder)
    logging.debug("Папка 'images' на рабочем столе удалена")

# Логирование завершения работы программы
logging.debug("Завершение работы программы")
