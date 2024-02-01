import sqlite3
from typing import List

def add_data_video(db, id_video:str) -> List:
    """
    Добавление в таблицу video_bd_table id video если нет, 
    а если есть то получаем id video в таблице video_bd_table
    и возвращаем id в таблице video_bd_table

    - id_video - id видео в ютубе
    """
    try:
        c =  db.cursor()
        #Запрос на вставление данных
        c.execute(' INSERT INTO video_bd_table (video)  VALUES (?)',(id_video,))
        db.commit()
    except sqlite3.IntegrityError:
        pass
    cur =  db.cursor()
    #Запрос на получение id
    cur.execute(f"""SELECT id FROM video_bd_table WHERE video == '{id_video}'""")
    result = cur.fetchall()
    return result


def add_data_athor(db, id_athor_channel:str) -> List:
    """
     Добавление в таблицу authorChannelId_bd_table id athor если нет, 
    а если есть то получаем id athor в таблице authorChannelId_bd_table
    и возвращаем id в таблице authorChannelId_bd_table

    - id_athor_channel - id автора канала
    """
    try:
        c = db.cursor()
        #Запрос на вставление данных
        c.execute('INSERT INTO authorChannelId_bd_table (authorChannelId) VALUES (?)',(id_athor_channel,))
        db.commit()
    except sqlite3.IntegrityError:
        pass
    cur =  db.cursor()
    #Запрос на получение id
    cur.execute(f"SELECT id FROM authorChannelId_bd_table WHERE authorChannelId == '{id_athor_channel}'")
    record =  cur.fetchall()
    return record


def insert_event(db, id_comment:str, id_video:str, id_channel:str, text_commment:str, publishedAt:str) -> None:
    """
    Функция для вставления в таблицу main_table данных

    - id_comment - id комментария в ютубе
    - id_video - id видео в ютубе
    - text_commment - текс комментария
    - id_channel -  id канала в ютубе
    - publishedAt - дата публикации
    """
    try:
      sql = """INSERT INTO main_table 
                (id_comment, id_video, id_channel, text_commment, publishedAt)  
                VALUES (?, ?, ?, ?, ?)"""
      db.execute(sql, (id_comment, id_video, id_channel, text_commment, publishedAt))
      db.commit()
    except:
        pass
    
    
def main(id_comment:str, id_video:str, id_channel:str, text_commment:str, publishedAt:str) -> None:
    """
    Функция для запуска записи

    - id_comment - id комментария в ютубе
    - id_video - id видео в ютубе
    - text_commment - текс комментария
    - id_channel -  id канала в ютубе
    - publishedAt - дата публикации
    """
    with sqlite3.connect('COMMENTS_MAIN.db') as db:
        id_in_db_author =  add_data_athor(db=db, id_athor_channel=id_channel)
        id_in_db_video =  add_data_video(db=db, id_video=id_video)
        insert_event(db, id_comment, id_in_db_video[0][0], id_in_db_author[0][0], text_commment, publishedAt)