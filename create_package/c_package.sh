#!/bin/bash
# Author: Arsenii Kostenko
# This script build C++ package
# Must be run on bash shell 
# Argument: ./c_package.sh my_package /path/to/directory

# Find package and tar
find_path() {

    # Ищим файл с информацией о сборке
    build_info_file=$(mktemp)
    # Если файл не существует, создаем его
    if [ ! -f "$1" ]; then
        touch "$1"
    fi
    
    cat > "$1" << EOF
    #!/bin/bash
    package_name="${1##*/}"
    absolute_path=$(cd .. && pwd)
    echo "Package name: ${package_name}"
    echo "Absolute path: ${absolute_path}"
    echo "Build information:"
    echo "================="
    echo "================================"
    echo "package_name: ${package_name}"
    echo "absolute_path: ${absolute_path}"
    echo "================================"
    EOF

    }

# Функция для создания пакета
create_package() {

    # Используем find для найти все файлы в директории
    find . -type f -name "BUILD_INFO.txt" -exec sh -c 'find_path "$1"' \;

    # Создаем пакет
    tar -czf "package_name".tar.gz -C "$absolute_path" .

}

# Если аргумент валидный, то выполняем функцию создания пакета
if [ "$1" != "" ]; then
    create_package

else
    # Если нет аргумента, то выводим сообщение об остановке
    echo "Usage: $0 <package_name> <absolute_path>"
fi
