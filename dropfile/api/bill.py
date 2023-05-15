import shutil
import zipfile
import os
import uuid
from loadFile.models import renderData


def extract_zip_file(file, user, fileid):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        extract_folder = os.path.join('/tmp', str(uuid.uuid4()))
        zip_ref.extractall(extract_folder)

        # Создание директории, если она не существует
        new_folder = os.path.join('media', 'users', str(user.id), 'files')
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

        # Обход всех файлов во временной папке
        for filename in os.listdir(extract_folder):
            # Полный путь к файлу
            file_path = os.path.join(extract_folder, filename)

            # Новое имя файла на основе UUID
            new_filename = str(uuid.uuid4()) + '.jpg'
            # Полный путь к новому файлу
            new_file_path = os.path.join(new_folder, new_filename)
            print(filename, new_file_path)
            render_data_obj = renderData.objects.create(fileLink=new_file_path)
            render_data_obj.fileid.add(fileid)
            # Переименование файла и перемещение в новую директорию
            os.rename(file_path, new_file_path)

        # Удаление временной папки
        shutil.rmtree(extract_folder)

