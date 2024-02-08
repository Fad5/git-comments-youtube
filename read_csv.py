from config import id_chanel
import csv
from config import main_dir
from def_work_database_video import Work_with_table_video, Work_with_data_in_table_video
from def_sql_db import main


def save(video_id, id_chanel):
    """
    Функция для сохранения id video в базу данныx, и сохранение всех данных с csv файла

    - video_id - видео id в ютубе
    - id_chanel- id канала в ютубе
    """
    Work_with_table_video.create_table(id_chanel=id_chanel)
    data = Work_with_data_in_table_video.get_id_video(id_chanel=id_chanel)
    if video_id in data:
        print('Пропуск')
        pass
    else:   
        print('Сохранение в базу данных!')
        with open(f'{main_dir}/{id_chanel}/{video_id}.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i in reader:
                main(id_comment=i["id"], id_video=video_id, id_channel=i["authorChannelId"], text_commment=i["textOriginal"], publishedAt=i["publishedAt"])
            print('Готово')
        Work_with_data_in_table_video.add_data(id_chanel=id_chanel,id_video = video_id)

        



