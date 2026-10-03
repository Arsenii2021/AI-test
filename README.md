# Arsenii Kostenko

Инженер: QA, Virtualization, ML, Linux/облако.

Репозиторий — не набор скриптов, а один контур: снимок консоли/UI → CNN → автотест → ONNX/C++ на хосте → стенд OpenNebula. Python, C++, bash, Terraform и Ansible связаны одним сценарием, а не живут отдельно.

**Контакты:** [GitHub](https://github.com/Arsenii2021) · [Hugging Face](https://huggingface.co/spaces/Arsenii2023/Linear_reg) · [elibrary: анализ изображений](https://www.elibrary.ru/item.asp?id=60234536) · [elibrary: автотесты в облачной виртуализации](https://elibrary.ru/item.asp?id=65485768)

---

## Образование

1. Бакалавриат по направлению «Инженер по качеству» в области информационно-аналитических систем.
2. Программа магистратуры «Анализ данных и искусственный интеллект» (ML).

## Опыт в разработке

1. Python, C++, PHP для автоматизации тестирования (Selenium + Python).
2. PyTorch, TensorFlow, ONNX для разработки нейросетей.
3. Нейросеть для анализа изображений на TensorFlow и PyTorch.
4. MLOps и деплой нейросетей в производственной среде.

## Опыт в тестировании и QA

1. Теория тестирования ПО.
2. Git (Terminal/Desktop).
3. Багтрекинг: Jira, загрузка материалов в TestIT.
4. Тестовые стратегии, планы и таблицы принятия решений.
5. MS/LibreOffice и офисный пакет для Mac.
6. Сертификаты GeekBrains.

## Опыт в администрировании

1. Linux (Debian).
2. Виртуальные среды: libvirt, QEMU/KVM, Virt-manager, Oracle VirtualBox.
3. Скрипты на bash.
4. Сети: мосты, DHCP, Apache2, DNS, зеркалирование трафика.
5. Домен: FreeIPA, Active Directory.
6. Установка ОС, BIOS/PXE/Live CD, Grub rescue.
7. OpenNebula, OpenStack; хранилища: Ceph, LVM, OCFS2, NFS.
8. Форматы ВМ (qcow2, ova) и конвертация.
9. Terraform для деплоя инфраструктуры OpenNebula.

## Прочие навыки

1. Английский: техническая документация, базовый разговорный.
2. MS Project: бизнес-процессы и ТЗ на разработку компонентов.

---


Описание проекта: снимок (`Selenium` или `virsh screenshot`) → классификация состояния консоли `boot | login | ready | error` → assert в CLI/pytest → экспорт ONNX → инференс на C++.

| Keras / OpenCV, датасет, обучение | `vision_qa/dataset.py`, `vision_qa/model.py`, `vision_qa/synth.py` |
| Selenium, автотест по изображению | `vision_qa/capture.py`, `python -m vision_qa infer --expect …` |
| ONNX, C++, прод-инференс | `python -m vision_qa export-onnx`, `cpp/infer.cpp` |
| pytest, CI | `tests/`, `.github/workflows/ci.yml` |
| OpenNebula + Terraform | `infra/terraform/` |
| Ansible, Linux-хосты | `infra/ansible/`, `infra/bash/host-upgrade.sh` |
| bash, KVM/libvirt | `infra/bash/`, `capture --domain` |

```
capture / synth  →  train (Keras)  →  infer (pytest)
                         ↓
                   export-onnx
                         ↓
                   cpp/infer (ONNX Runtime + OpenCV)
                         ↑
            infra: Terraform VM + Ansible frontend
```

### Запуск

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,train,capture]"
python -m vision_qa synth
python -m vision_qa train --epochs 8
python -m vision_qa infer data/screens/ready/ready_000.png --expect ready
python -m vision_qa export-onnx
python -m vision_qa capture --url https://example.com --out /tmp/ui.png
python -m vision_qa capture --domain guest01 --out /tmp/console.png
pytest
```

C++ (OpenCV и [ONNX Runtime](https://github.com/microsoft/onnxruntime)):

```bash
cmake -S cpp -B cpp/build -DONNXRUNTIME_ROOT=/opt/onnxruntime
cmake --build cpp/build
./cpp/build/infer models/ui.onnx /tmp/console.png
```

OpenNebula:

```bash
cp infra/terraform/terraform.tfvars.example infra/terraform/terraform.tfvars
# пароль: TF_VAR_password, не git
infra/terraform/apply.sh
```
