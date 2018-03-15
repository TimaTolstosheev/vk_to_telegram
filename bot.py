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

#------------Файлом Телеграм разрешает отправить только контент не более 20Мб,
#------------поэтому отправить видео = отправить сообщение с текстом, где разрешено превью контента. 
def send_video(video_url, message_text=None):
    url = 'https://api.telegram.org/bot' + config.telegram_token + '/sendMessage'
    parameters = {'chat_id': config.chat_id,
                  'text': video_url,
                  'disable_web_page_preview': False}
    r = get(url, params=parameters)
    return r

def send_media_group(media_urls):
    url = 'https://api.telegram.org/bot' + config.telegram_token + '/sendMediaGroup'
    parameters = {'chat_id': config.chat_id,
                  'media': json.dumps(media_urls)}
    r = get(url, params=parameters)
    return r

if __name__ == '__main__':
    posted_records_hashes = []
    while True:
        for group in config.vk_group_ids:
            wall_record_data = get_data_from_last_wall_record(config.vk_group_ids)
            record_hash = hash(repr(wall_record_data.items()))
            if record_hash in posted_records_hashes:
                continue
            else:
                posted_records_hashes.append(record_hash)
                message_text = wall_record_data['text'].replace("<br>", '\n')
                #---Списки images и videos в wall_record_data будут в любом случае, поэтому проверяем на их длину
                if len(wall_record_data['images']) > 0:
                    if len(wall_record_data['images']) > 1:
                        send_media_group(wall_record_data['images'])
                        continue
                    if len(message_text) > 200:
                        send_image(wall_record_data['images'])
                    else:
                        send_image(wall_record_data['images'], message_text)
                        continue
                if len(wall_record_data['videos']) > 0:
                    for video in wall_record_data['videos']: #----каждое видео постится отдельным сообщением, потому что превьюится только первое
                        send_video(video)
                send_message(message_text)
        if len(posted_records_hashes) > 100:
            del posted_records_hashes[0]
        sleep(30)
