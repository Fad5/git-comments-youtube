import sqlite3


class Work_with_db_video:
    def create_db(id_chanel:str,id_user = "list_vidos") -> sqlite3.Cursor:
        """
        Функция для создания базы данных

        - 
        """
        with sqlite3.connect(f'csv/{id_chanel}/{id_user}.db') as db:
            cursor = db.cursor()
            return cursor


class Work_with_table_video:
    def create_table(id_chanel: str, name_table: str = 'message') -> None:
        """
        Функция для создания таблицы
        """
        cursor = Work_with_db_video.create_db(id_chanel)
        query = f""" CREATE TABLE IF NOT EXISTS {name_table} (
            id_video TEXT
        )"""
        cursor.execute(query)



class Work_with_data_in_table_video:
    def add_data(id_chanel:str, id_video: str):
        """
        """
        db = sqlite3.connect(f'csv/{id_chanel}/list_vidos.db')
        sql = db.cursor()
        sql.execute(f"INSERT INTO message (id_video) VALUES ('{id_video}') ")
        db.commit()
        db.close()


    def get_id_comments(id_chanel:str) -> list:
        """
        """
        list_id = []
        db = sqlite3.connect(f'csv/{id_chanel}/list_vidos.db')
        sql = db.cursor()
        sql.execute(f"""SELECT id_video FROM message""")
        for i in sql:
            list_id.append(i[0])
        return list_id
