import os
import time
from datetime   import datetime


def get_info_file():
    """
    Получение размера файла
    """
    file_info = os.stat('COMMENTS_MAIN.db')
    file_size = file_info.st_size
    return file_size / 1048576


def create_dir_if_is_none(name_dir:str):
    list_dir = os.listdir()
    if name_dir in list_dir:
        pass
    else:
        os.mkdir('csv')


def create_dir_сhenel_if_is_none(name_dir:str):
    list_dir = os.listdir('csv/')
    print(list_dir)
    if name_dir in list_dir:
        pass
    else:
        os.mkdir(f'csv/{name_dir}')
