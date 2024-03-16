#!/bin/bash
#Author:Arsenii Kostenko

# Цвета для вывода
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Функция для вывода информации
info() {
  echo -e "${GREEN}$1${NC}"
}

# Планирование Terraform
info "Планируем конфигурацию Terraform..."
terraform plan > /dev/null 2>&1
if [ $? -eq 0 ]; then
    info "Планирование завершено успешно."
else
    echo "Ошибка при планировании Terraform."
    exit 1
fi

# Инициализация Terraform
info "Инициализируем конфигурацию Terraform..."
terraform init > /dev/null 2>&1
if [ $? -eq 0 ]; then
    info "Инициализация завершена успешно."
else
    echo "Ошибка при инициализации Terraform."
    exit 1
fi

# Применение конфигурации с auto-approve
info "Применяем конфигурацию Terraform..."
terraform apply -auto-approve > /dev/null 2>&1
if [ $? -eq 0 ]; then
    info "Конфигурация применена успешно."
else
    echo "Ошибка при применении конфигурации Terraform."
    exit 1
fi
