import time
import csv
import os
import json
import googleapiclient.discovery
import googleapiclient.errors 
from config import id_chanel, list_token, main_dir
from read_csv import save
from info_file import create_dir_if_is_none,create_dir_сhenel_if_is_none
from get_video_in_chanel import get_file_json

#Создание папки csv если нет
create_dir_if_is_none(name_dir='csv')

create_dir_сhenel_if_is_none(name_dir=id_chanel)

#Сохранение в список видео которые были уже обработаны
list_sort_id_video: list = []

#Получение список файлов которые есть в папке 
list_files = os.listdir(f'{main_dir}/{id_chanel}')


def youtube(video_id:str, token:str, nextPageToken=None):
    """
    Функция для скачивания корневых комментариев

    - video_id - id видео в ютубе
    - token - ваш токен
    - nextPageToken - токен для получения следующих данных (по умолчанию None)
    """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=token)

    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
        pageToken=nextPageToken,
        videoId=video_id
    )
    response = request.execute()
    return response


# Главная функция
def main(video_id, token, path=main_dir):
    # Скачиваем комментарии
    print('download comments')
    response = youtube(video_id=video_id, token=token)
    items = response.get("items")
    nextPageToken = response.get("nextPageToken")  # скачивается порциями, на каждую следующую выдаётся указатель
    i = 1
    while nextPageToken is not None:
        print(str(i * 100))  # показываем какая сотня комментариев сейчас скачивается
        response = youtube(video_id, token, nextPageToken)
        nextPageToken = response.get("nextPageToken")
        items = items + response.get("items")
        i += 1

    print(len(items))  # Отображаем количество скачаных комментариев

    # Скачиваем реплаи на комментарии
    print('download replies')
    replies = []
    for line in items:  # Проходим по корневым комментам
        if line.get("snippet").get("totalReplyCount") > 0:  # если есть реплаи
            replies = replies + response.get("items")
            nextPageToken = response.get("nextPageToken")
            i = 1
            while nextPageToken is not None:  # догружаем реплаи, если есть ещё порции
                nextPageToken = response.get("nextPageToken")
                replies = replies + response.get("items")
                i += 1

    # Сохраняем комментарии и реплаи на них в файл csv
    print("Open csv file")
    with open(f'{path}{video_id}.csv', 'w',
              encoding="utf-8") as csv_file:  # конструкция with, чтобы файл закрылся автоматом после всех команд
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL,
                            lineterminator='\r')  # использовал двойные кавычки и разделитель запятую, такой формат отлично открывается через LibreOffice Calc

        # Заголовки столбцов
        row = [
            'etag'
            , 'parentid'
            , 'id'
            , 'textDisplay'
            , 'textOriginal'
            , 'authorDisplayName'
            , 'authorProfileImageUrl'
            , 'authorChannelUrl'
            , 'authorChannelId'
            , 'likeCount'
            , 'publishedAt'
            , 'updatedAt'
        ]
        writer.writerow(row)  # Записываем заголовки в файл

        # Сохраняем комментарии
        print("Write comments in csv")
        for line in items:
            topLevelComment = line.get("snippet").get("topLevelComment")
            if topLevelComment.get('snippet').get('authorChannelId') is not None:
                authorChannelId = topLevelComment.get('snippet').get('authorChannelId').get('value')
            else:
                authorChannelId = ''
            row = [
                topLevelComment.get('etag')
                , topLevelComment.get('id')
                , topLevelComment.get('id')
                , topLevelComment.get('snippet').get('textDisplay')
                , topLevelComment.get('snippet').get('textOriginal')
                , topLevelComment.get('snippet').get('authorDisplayName')
                , topLevelComment.get('snippet').get('authorProfileImageUrl')
                , topLevelComment.get('snippet').get('authorChannelUrl')
                , authorChannelId
                , topLevelComment.get('snippet').get('likeCount')
                , topLevelComment.get('snippet').get('publishedAt')
                , topLevelComment.get('snippet').get('updatedAt')
            ]
            writer.writerow(row)

        # Сохраняем реплаи
        print("Write replies in csv")



def video_list():
    """
    Функия придназначена для считывания id видео по которому будет искать комментарии
    return: список id видео 
    """
    with open(f'{main_dir}/{id_chanel}/{id_chanel}_videos.json', 'r') as file:
        data = json.load(file)
    videos_list = []
    for i in data:
        videos_list.append(i['video_id'])
    return videos_list


def get_files():
    """
    Функция для получение существующих csv файлов
    return: список существующих csv файлов в названии id видео 
    """
    list_files = os.listdir(f'{main_dir}/{id_chanel}')
    list_current_video = []
    list_videos = video_list()
    for id_videdo in list_videos:
        current_i = f'{id_videdo}.csv'
        if current_i in list_files:
            pass
        else:
            list_current_video.append(id_videdo)
    return list_current_video


def procent_error(count, count_error):
    """
    Процентный счетчик 
    """
    if count_error == 0:
        return '0'
    if count == 0:
        return '0'
    else:
        result = 100 - (count_error / count * 100) 
        return result


def start():
    token_number = 0
    # Создания json файла
    get_file_json()
    error_count = 0
    # список id_video
    data = get_files()
    t = 0
    conut = 0
    len_vi = len(data)
    for video_id in data:
        t = t + 1
        procent = procent_error(conut, error_count)
        print(f'{t} of {len_vi} \nError: {error_count} из {conut} \nSucessfull: {procent} ')
        try:
            conut = conut + 1
            # Добыча информации 
            main(video_id, list_token[token_number], f'{main_dir}/{id_chanel}/')
            # Сохранение
            save(video_id=video_id, id_chanel=id_chanel, path=main_dir)

        except TimeoutError:
            # Увеличение счеткика ошибок
            error_count = error_count + 1 
            # Увеличение индекса в списке при ошибке 
            token_number = token_number + 1
            print('TimeoutError')
            time.sleep(10)
            pass

start()
