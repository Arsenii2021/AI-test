import os

def install_docker():
    # Обновляем список пакетов
    os.system("sudo apt update")

    # Устанавливаем необходимые пакеты для установки Docker
    os.system("sudo apt install -y apt-transport-https ca-certificates curl software-properties-common")

    # Добавляем официальный GPG ключ Docker
    os.system("curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -")

    # Добавляем репозиторий Docker в список источников пакетов
    os.system('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"')

    # Обновляем список пакетов с учетом нового репозитория Docker
    os.system("sudo apt update")

    # Устанавливаем Docker
    os.system("sudo apt install -y docker-ce")

    # Добавляем текущего пользователя в группу docker, чтобы не использовать sudo при запуске команд Docker
    os.system("sudo usermod -aG docker $USER")

    print("Docker успешно установлен и настроен.")

# Запускаем функцию установки Docker
install_docker()
