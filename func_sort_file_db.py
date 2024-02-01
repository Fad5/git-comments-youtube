import os
import shutil


def files_db(path_dir):
    """
    Функция files_db принимает название или путь папки и возврашает список
    """
    list_db_fils = os.listdir(path_dir)
    return list_db_fils
    

def sort_symbols_in_files(list_db_fils):
    """
    В функии sort_symbols_in_files создается пустой список, какда помешаются 3ий символ найзвания db
    и потом сортируется убирая дубликаты, возвращает отсортированные символы
    """
    list_name_db_fils = []
    for i in list_db_fils:
        if i =='.db':
            pass
        else:
            symbol_3_name = i[2].upper()
            list_name_db_fils.append(symbol_3_name)
    sort_symbols = (set(list_name_db_fils))
    return sort_symbols


def create_dir(symbol,path):
    """
    Создает папку по имени символа 
    """
    try:
        os.mkdir(f'{path}/{symbol}')
    except:
        pass


def check_dir(name_dir):
    """
    Проверка на существования папки
    """
    list_dir = os.listdir()
    if name_dir in list_dir:
        pass
    else:
        os.mkdir(f'{name_dir}')


def move_file(name_file):
    symbol_file = name_file[2]
    list_dir = os.listdir('sort_users')
    if symbol_file.upper() in list_dir:
        print('ok')
        print(f'sort_users\{symbol_file.upper()}\{name_file}')
        shutil.copy(f'users\{name_file}', f'sort_users\{symbol_file.upper()}\{name_file}')
    elif symbol_file.upper() not in list_dir:
        os.mkdir(f'{symbol_file.upper()}')
        shutil.copy(f'users\{name_file}', f'sort_users\{symbol_file.upper()}\{name_file}')
    else:
        pass


def main():
    count = 0
    name_dir = "sort_users"
    check_dir(name_dir)
    files_db_list = files_db('users')
    sort_symbols = sort_symbols_in_files(files_db_list)
    print(sort_symbols)
    print(len(sort_symbols))
    for symbol in sort_symbols:
        create_dir(symbol,name_dir)
    for i in files_db_list:
        count = count + 1
        move_file(i)
        print(f'{count} of {len(files_db_list)}')

main()



