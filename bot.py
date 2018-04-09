import config
import json

from time import sleep
from requests import get
from vk_wall_listener import get_data_from_last_wall_record

from flask import Flask
from flask import render_template
from flask import request

def send_message(message_text):
    url = 'https://api.telegram.org/bot' + config.telegram_token + '/sendMessage'
    parameters = {'chat_id': config.chat_id,
                  'text': message_text,
                  'disable_web_page_preview': True}
    r = get(url, params=parameters)
    return r


def send_image(image_url, message_text=None):
    url = 'https://api.telegram.org/bot' + config.telegram_token + '/sendPhoto'
    parameters = {'chat_id': config.chat_id,
                  'photo': image_url}
    if message_text:
        parameters['caption'] = message_text
    else:
        parameters['disable_notification'] = True
    r = get(url, params=parameters)
    return r


def send_media_group(media_urls):
    input_media_list = list()
    for url in media_urls:
        input_media_list.append({'type':'photo','media':url})
    url = 'https://api.telegram.org/bot' + config.telegram_token + '/sendMediaGroup'
    parameters = {'chat_id': config.chat_id,
                  'media': json.dumps(input_media_list)}
    r = get(url, params=parameters)
    return r

#------------Файлом Телеграм разрешает отправить только контент не более 20Мб,
#------------поэтому отправить видео = отправить сообщение с текстом, где разрешено превью контента.
def send_video(video_url):
    url = 'https://api.telegram.org/bot' + config.telegram_token + '/sendMessage'
    parameters = {'chat_id': config.chat_id,
                  'text': video_url,
                  'disable_web_page_preview': False}
    r = get(url, params=parameters)
    return r

def has_already_been_reposted(record, chat):
    hashes = get_posted_hashes(chat)
    ids = get_posted_ids(chat)
    if ((record['hash'] in hashes)
            or (record['record_id'] in ids)
            or ((record['original_record_id'] != None)
                    and (record['original_record_id'] in ids))):
        return True
    else:
        return False


def get_posted_hashes(chat):
    return posted_records_hashes
    # заменить потом на нормальную имплементацию с БД

def get_posted_ids(chat):
    return posted_records_ids
    # заменить потом на нормальную имплементацию с БД

def get_posted_original_ids(chat):
    return posted_records_original_ids
    # заменить потом на нормальную имплементацию с БД


def add_record_to_posted(record, chat):
    add_hash_to_posted(record['hash'], chat)
    add_id_to_posted(record['record_id'], chat)
    if record['original_record_id'] != None:
        add_id_to_posted(record['original_record_id'], chat)    # NB! я намеренно сливаю и id конечных постов, и id оригинальных постов в одно место (для чего — см. ниже)
    # тут мы проверяем на выполнение любого условия, приводящего к отмене переброса в Телеграм:
    # — либо такое содержимое уже перебрасывали
    #       (определяем по хешу, учитывающему: а) текст, б) объём каждой картинки
    #       в любом порядке, если есть картинки; подробнее см. в calculate_hash_for_record())
    # — либо перпебрасывали тот же самый пост, который сейчас пытаемся перебросить
    #       (определяем по id этого поста)
    # — либо перебрасывали репост того же самого оригинального поста
    #       или тот же пост, репост которого сейчас пытаемся перебросить
    #       (определяем по id этого и id оригинального поста, сравнивая с общей базой id)

def add_hash_to_posted(new_hash, chat):
    posted_records_hashes.append(new_hash)    # пока возвращаем временный общий список; заменить потом на нормальную имплементацию

def add_id_to_posted(new_id, chat):
    posted_records_ids.append(new_id)    # то же самое

posted_records_hashes = []
posted_records_ids = []
def repost(group):#все засовываем в функцию, которая вызывается, как только сервер получает post
    current_chat = config.chat_id    # потом надо будет подставлять сюда каждый чат отдельно, если мы хотим добавить работу с разными чатами
    current_record = get_data_from_last_wall_record(group)
    if not(has_already_been_reposted(current_record, current_chat)):
        add_record_to_posted(current_record, current_chat)
        message_text = current_record['text'].replace("<br>", '\n')
        if 'pictures' in current_record:
            if len(current_record['pictures']) > 1:
                send_media_group(current_record['pictures'])
            if len(message_text) < 200:
                send_image(current_record['pictures'], message_text)
            else:
                send_image(current_record['pictures'])
        if 'videos' in current_record:
            for video in current_record['videos']: #----каждое видео постится отдельным сообщением, потому что превьюится только первое
                send_video(video)
        send_message(message_text)
    if len(posted_records_hashes) > 100:
        del posted_records_hashes[0]    # это точно надо будет куда-то выводить отдельно, особенно когда это уже будет не временная переменная, а БД"""
    return 'ok' #VK требует возврата 'ok' в ответ на callback

#---Flask-server---
app = Flask(__name__)

secret_key = config.secret_callback_key #ключ для настройки коллбэков. Можно прописать в конфиге

@app.route('/bot', methods=['POST','GET']) # на этот адрес VK должен отправлять колбэки
def bot():
    if request.method == 'POST':
        content=request.get_json()
        if content['type'] == 'confirmation': return secret_key #ответ на подтверждение использования колбэков
        elif content['type'] == 'wall_post_new':
            group=content['group_id']
            return repost(group) #на событие нового поста вызывается repost()
        else: return('ok')#на любой другой колбэк от vk
    if request.method=='GET': return ('ok')

@app.route('/', methods=['POST','GET']) # на этот адрес VK должен отправлять колбэки
def home():return 'ok'

if __name__== '__main__': app.run(host='0.0.0.0', port=int("80"))
