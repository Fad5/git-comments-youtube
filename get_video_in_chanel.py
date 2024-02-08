import json
import os
from googleapiclient.discovery import build
from config import id_chanel



def create_dir(id_chanel) -> None:
    list_dir = os.listdir('csv')
    if id_chanel not in list_dir:
        os.mkdir(f'csv/{id_chanel}')

def get_file_json():
    create_dir(id_chanel=id_chanel)
    # Получение id пейлиста канала в котром все видео
    service_simple = build('youtube', 'v3', developerKey='AIzaSyBoYFxTpFia5Hc-j8wDhWA1QSaWqFCTE34')
    r = service_simple.channels().list(id=id_chanel, part='contentDetails').execute()
    uploads_playlist = r['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = []
    
    args = {
        'playlistId': uploads_playlist,
        'part': 'contentDetails',
        'maxResults': 5
    }
    for _ in range(0, 200):
        r = service_simple.playlistItems().list(**args).execute()
        print(r.get('nextPageToken'))
        for item in r['items']:
            id_video = item['contentDetails']['videoId']
            videos.append({
                'video_id': id_video
            })
        args['pageToken'] = r.get('nextPageToken')
        if not args['pageToken']: break
    
    with open(f'csv/{id_chanel}/{id_chanel}_videos.json', 'w') as file:
        json.dump(videos, file)
    