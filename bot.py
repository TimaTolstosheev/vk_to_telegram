import config
import json

from time import sleep
from requests import get
from vk_wall_listener import get_data_from_last_wall_record


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

def test(value=''):
    return value

def repost():#все засовываем в функцию, которая вызывается, как только сервер получает post
    posted_records_hashes = []
    posted_records_ids = []
    current_chat = config.chat_id    # потом надо будет подставлять сюда каждый чат отдельно, если мы хотим добавить работу с разными чатами
    return 'Starting infinite while'
    while True:
        for group in config.vk_group_ids:
            current_record = get_data_from_last_wall_record(group)
            if has_already_been_reposted(current_record, current_chat):
                continue
            else:
                add_record_to_posted(current_record, current_chat)
                message_text = current_record['text'].replace("<br>", '\n')
                if 'images' in current_record:
                    if len(current_record['images']) > 1:
                        send_media_group(current_record['images'])
                        continue
                    if len(message_text) < 200:
                        send_image(current_record['images'], message_text)
                        continue
                    else:
                        send_image(current_record['images'])
                send_message(message_text)
        if len(posted_records_hashes) > 100:
            del posted_records_hashes[0]    # это точно надо будет куда-то выводить отдельно, особенно когда это уже будет не временная переменная, а БД
        sleep(30)
