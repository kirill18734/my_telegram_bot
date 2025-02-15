import json
import os


# Объединенная функция для автоматического поиска файла
def find_file_in_project(filename, search_path):
    for root_dir, dirs, files in os.walk(search_path):
        for file in files:
            if file == filename or (
                    file.lower() == filename.lower() and
                    file[0].istitle()):  # два пробела перед символом '#'
                return os.path.join(root_dir, file)

def read_files_text(files):
    with open(files, 'r', encoding='utf-8') as r:
        return r.read()

# Путь до текущей папки
path_to_current_folder = os.path.dirname(os.path.realpath(__file__))

# Путь до папки проекта
path_to_project_folder = os.path.dirname(path_to_current_folder)
# Название папки проекта
project_folder_name = os.path.basename(path_to_project_folder)

# находим основной запускающий файл
path_to_main = find_file_in_project(f'{project_folder_name}.py',
                                    path_to_project_folder)

# Ищем файл python.exe
path_to_python_exe = find_file_in_project('python.exe',
                                          path_to_project_folder)

# Ищем файл config.json и получаем его путь
path_to_config_json = find_file_in_project('config.json',
                                           path_to_project_folder)

# Ищем файл config.json и получаем его путь
path_to_users_json = find_file_in_project('user_ids.json',
                                           path_to_project_folder)
# Ищем файл config.json и получаем его путь
path_db = find_file_in_project('data_grafic.db',
                                           path_to_project_folder)

path_to_img = find_file_in_project('months.png',
                                   path_to_project_folder)
# атака
file_volley_attack= find_file_in_project('attack.txt', path_to_project_folder)
volley_attack = read_files_text(file_volley_attack)
# пасс
file_volley_pass= find_file_in_project('pass.txt', path_to_project_folder)
volley_pass = read_files_text(file_volley_pass)
# прием
file_volley_preception= find_file_in_project('preception.txt', path_to_project_folder)
volley_preception = read_files_text(file_volley_preception)
# подача
file_volley_supply= find_file_in_project('supply.txt', path_to_project_folder)
volley_supply = read_files_text(file_volley_supply)
# овощной суп
file_vegetable_soup = find_file_in_project('vegetable_soup.txt', path_to_project_folder)
vegetable_soup = read_files_text(file_vegetable_soup)
# борщ суп
file_borscht_sup = find_file_in_project('borscht_sup.txt', path_to_project_folder)
borscht_sup = read_files_text(file_borscht_sup)

# Преобразуем содержимое файла
with open(path_to_config_json, 'r', encoding='utf-8') as file:
    data_config = json.load(file)
