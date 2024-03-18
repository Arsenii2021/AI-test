import docker

def create_container(image_name, container_name):
    # Создаем клиент Docker
    client = docker.from_env()

    try:
        # Пытаемся создать контейнер из указанного образа
        container = client.containers.run(image=image_name, detach=True, name=container_name)
        print(f"Контейнер {container_name} успешно создан.")
    except docker.errors.ImageNotFound:
        print(f"Образ {image_name} не найден.")
    except docker.errors.APIError as e:
        print(f"Ошибка API Docker: {e}")

# Пример использования
if __name__ == "__main__":
    image_name = "nginx:latest"  # Имя образа
    container_name = "my-nginx"  # Имя контейнера
    create_container(image_name, container_name)
