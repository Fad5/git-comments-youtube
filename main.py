import time
import csv
import os
import json
import googleapiclient.discovery
import googleapiclient.errors as google_errors
from config import id_chanel, list_token
from read_csv import save

#Сохранение в список видео которые были уже обработаны
list_sort_id_video = []

list_files = os.listdir(f'csv/{id_chanel}')


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
def main(video_id, token, path='csv/'):
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

    print(len(replies))  # Отображаем количество скачаных реплаев

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
    with open(f'csv/{id_chanel}/{id_chanel}_videos.json', 'r') as file:
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
    list_filess = os.listdir(f'csv/{id_chanel}')
    list_current_video = []
    for i in list_filess:
        element = i[:-4]
        list_current_video.append(element)
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
    error_count = 0
    data = video_list()
    list_videos = get_files()
    t = 0
    conut = 0
    len_vi = len(data)
    print(len_vi)
    for i in data:
        t = t + 1
        procent = procent_error(conut, error_count)
        print(f'{t} of {len_vi}')
        print(f'Error: {error_count} из {conut}')
        print(f'Sucessfull: {procent} %')
        if i in list_videos:
            pass
        else:
            try:
                conut = conut + 1
                main(i, list_token[-4], f'csv/{id_chanel}/')
                save(i,f'csv/{id_chanel}/')
    
            except TimeoutError:
                error_count = error_count + 1 
                print('TimeoutError')
                time.sleep(10)
                pass

start()
