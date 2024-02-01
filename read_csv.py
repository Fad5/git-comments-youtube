from config import id_chanels
import csv
from def_work_database_video import Work_with_table_video, Work_with_data_in_table_video
from def_sql_db import main
import os


def save(video_id, path='csv/'):
    with open(f'{path}{video_id}.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i in reader:
            main(id_comment=i["id"], id_video=video_id, id_channel=i["authorChannelId"], text_commment=i["textOriginal"], publishedAt=i["publishedAt"])
        print('Готово')


def list_read_csv(path_video,id_chanel):
    list_fails = os.listdir(path_video)
    len_fails = len(list_fails)
    count = 0
    Work_with_table_video.create_table(id_chanel=id_chanel)
    data = Work_with_data_in_table_video.get_id_comments(id_chanel=id_chanel)
    for i in list_fails:
            if i[-3:] == 'csv':
                    if i in data:
                        count = count + 1
                        print('Пропуск', count)
                        pass
                    else:
                        count = count + 1
                        info_scv = (f'{count} from {len_fails}')
                        print(info_scv)
                        correct_i = i[:-4]
                        save(correct_i,path_video)
                        Work_with_data_in_table_video.add_data(id_chanel=id_chanel,id_video = i)

for id_chanel in id_chanels:
    print(id_chanel) 
    path_video = f'csv/{id_chanel}/'
    list_read_csv(path_video=path_video,id_chanel=id_chanel)


