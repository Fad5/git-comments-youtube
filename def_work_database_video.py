import sqlite3


class Work_with_db_video:
    @staticmethod
    def create_db(id_chanel:str, db_name = "list_vidos") -> sqlite3.Cursor:
        """
        Функция для создания базы данных

        - id_chanel - id канала на ютубе
        - db_name - названия базы данных 
        """
        with sqlite3.connect(f'csv/{id_chanel}/{db_name}.db') as db:
            cursor = db.cursor()
            return cursor


class Work_with_table_video:
    @staticmethod
    def create_table(id_chanel: str, name_table: str = 'message') -> None:
        """
        Функция для создания таблицы

        - id_chanel - id канала на ютубе
        - name_table - названия таблицы
        """
        cursor = Work_with_db_video.create_db(id_chanel)
        query = f""" CREATE TABLE IF NOT EXISTS {name_table} (
            id_video TEXT
        )"""
        cursor.execute(query)



class Work_with_data_in_table_video:
    @staticmethod
    def add_data(id_chanel:str, id_video: str):
        """
        Функция для добавления информации 

        id_chanel - id канала на ютубе
        id_video - id видео на ютубе
        """
        db = sqlite3.connect(f'csv/{id_chanel}/list_vidos.db')
        sql = db.cursor()
        sql.execute(f"INSERT INTO message (id_video) VALUES ('{id_video}') ")
        db.commit()
        db.close()


    @staticmethod
    def get_id_video(id_chanel:str) -> list:
        """
        Получение id video 

        - id_chanel - id канала на ютубе
        """
        list_id = []
        db = sqlite3.connect(f'csv/{id_chanel}/list_vidos.db')
        sql = db.cursor()
        sql.execute(f"""SELECT id_video FROM message""")
        for i in sql:
            list_id.append(i[0])
        return list_id
