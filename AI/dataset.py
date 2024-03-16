# Author: Arsenii Kostenko
import pandas as pd
import tensorflow as tf

# images_array - массив с обучающими изображениями
# labels - метки классов для каждого изображения

# Созд списка с данными
data = {
    'Имя': ['VM1', 'Database2', 'Website3'],
    'Тип': ['Виртуальная машина', 'База данных', 'Веб-сайт'],
    'Описание': ['ОС: Ubuntu, Версия: 18.04', 'SQL Server, Версия: 2019', 'Электронный коммерция, PHP, MySQL'],
    'URL': ['ссылка_на_VM1', 'ссылка_на_Database2', 'ссылка_на_Website3'],
    'Теги': ['Linux', 'SQL', 'E-commerce']
}

# Создание DataFrame
df = pd.DataFrame(data)

# Добавление столбца с изображениями
df['Изображения'] = images_array

# Добавление столбца с метками классов
df['Метки'] = labels

# Вывод первых строк DataFrame
print(df.head())

# Сохранение датасета в файл
df.to_csv('название_файла.csv', index=False)
