# This script builds packages for python
# Argument: python create_package.py мойПакет /путь/к/директории "Информация о сборке 202 
# Author: Arsenii Kostenko

import subprocess
import sys
import os

def create_tar_package(package_name, absolute_path, build_info):
    """
    Создает архив tar из указанной директории.

    :param package_name: Название пакета (архива).
    :param absolute_path: Абсолютный путь к директории для архивации.
    :param build_info: Строка с информацией о сборке, которая добавляется в файл внутри архива.
    """
    # Создаем файл с информацией о сборке
    build_info_file = os.path.join(absolute_path, "BUILD_INFO.txt")
    with open(build_info_file, "w") as info_file:
        info_file.write(build_info)
    
    # Формируем команду для создания архива
    tar_command = ["tar", "-czvf", package_name + ".tar.gz", "-C", absolute_path, "."]

    try:
        # Выполнение команды создания архива
        subprocess.check_call(tar_command)
        print(f"Пакет {package_name}.tar.gz успешно создан.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании пакета: {e}")
    finally:
        # Удаляем временный файл с информацией о сборке
        os.remove(build_info_file)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python script.py <Название> <Путь> <Информация для сборки>")
        sys.exit(1)

    package_name = sys.argv[1]
    absolute_path = sys.argv[2]
    build_info = sys.argv[3]

    # Валидация существования директории
    if not os.path.isdir(absolute_path):
        print("Указанный путь не существует или не является директорией.")
        sys.exit(1)

    create_tar_package(package_name, absolute_path, build_info)
