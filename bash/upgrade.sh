#!/bin/bash
# Author: Arsenii Kostenko

# Определение цветов
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Проверка текущей директории
if [[ "$(basename "$(pwd)")" != "$HOME/upgrade" ]]; then
    echo -e "${RED}Ошибка:${NC} Скрипт должен быть запущен из директории 'upgrade'."
    echo -e "${YELLOW}Пожалуйста, перейдите в нужную директорию и запустите скрипт снова.${NC}"
    echo -e "${YELLOW}Текущая директория: $(pwd)${NC}"
    exit 1
fi

# Переменные с адресными пространствами
NODE_IP="192.168.1.1"
DEBIAN_USER="user"
DEBIAN_PASS="password"
UBUNTU_USER="user"
UBUNTU_PASS="password"
FEDORA_USER="user"
FEDORA_PASS="password"

# Функция для обновления системы Debian
update_debian() {
    sshpass -p "$DEBIAN_PASS" ssh "$DEBIAN_USER@$NODE_IP" "sudo apt update && sudo apt upgrade -y"
}

# Функция для обновления системы Ubuntu
update_ubuntu() {
    sshpass -p "$UBUNTU_PASS" ssh "$UBUNTU_USER@$NODE_IP" "sudo apt update && sudo apt upgrade -y"
}

# Функция для обновления системы Fedora
update_fedora() {
    sshpass -p "$FEDORA_PASS" ssh "$FEDORA_USER@$NODE_IP" "sudo dnf upgrade -y"
}

# Функция для проверки и установки grub
setup_grub() {
    read -p "На какой диск установить GRUB? (например, /dev/sda): " disk
    sshpass -p "$DEBIAN_PASS" ssh "$DEBIAN_USER@$NODE_IP" "sudo grub-install $disk"
}

# Функция для подключения репозиториев
add_repositories() {
    read -p "Сколько репозиториев вы хотите добавить? " count
    for ((i = 1; i <= count; i++)); do
        read -p "Введите URL репозитория $i: " repo_url
        sshpass -p "$DEBIAN_PASS" ssh "$DEBIAN_USER@$NODE_IP" "sudo add-apt-repository $repo_url"
    done
}

# Функция для обновления ядра (удаление или установка)
update_kernel() {
    sshpass -p "$DEBIAN_PASS" ssh "$DEBIAN_USER@$NODE_IP" "sudo apt install --install-recommends linux-generic-hwe-20.04"
}

# Главное меню
while true; do
    echo -e "${YELLOW}Выберите действие:${NC}"
    echo "1. Обновить Debian"
    echo "2. Обновить Ubuntu"
    echo "3. Обновить Fedora"
    echo "4. Проверить и настроить GRUB"
    echo "5. Добавить репозитории"
    echo "6. Обновить ядро"
    echo "0. Выйти"

    read -p "Введите номер действия: " choice

    case $choice in
    1)
        update_debian
        ;;
    2)
        update_ubuntu
        ;;
    3)
        update_fedora
        ;;
    4)
        setup_grub
        ;;
    5)
        add_repositories
        ;;
    6)
        update_kernel
        ;;
    0)
        echo "До свидания!"
        exit 0
        ;;
    *)
        echo -e "${RED}Ошибка:${NC} Неверный выбор. Пожалуйста, выберите действие из списка."
        ;;
    esac
done
