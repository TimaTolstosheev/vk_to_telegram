import config
import hashlib

from time import sleep
from requests import get
from vk_wall_listener import get_data_from_last_wall_record


def send_message(message_text):
    url = 'https://api.telegram.org/bot' + config.telegram_token + '/sendMessage'
    parameters = {'chat_id': config.chat_id,
                  'text': message_text,
                  'disable_web_page_preview': True}
    r = get(url, params=parameters)
    print("send_message status:", r)


def send_image(image_url):
    url = 'https://api.telegram.org/bot' + config.telegram_token + '/sendPhoto'
    parameters = {'chat_id': config.chat_id,
                  'photo': image_url,
                  'disable_notification': True}
    r = get(url, params=parameters)
    print("send_image status:", r)


if __name__ == '__main__':
    posted_records_hashes = []
    while True:
        for group in config.vk_group_ids:
            wall_record_data = get_data_from_last_wall_record(group)
            record_hash = hashlib.md5(wall_record_data['text'].encode()).hexdigest()
            if record_hash in posted_records_hashes:
                continue
            else:
                send_message(wall_record_data['text'].replace("<br>", '\n'))
                if 'image' in wall_record_data:
                    send_image(wall_record_data['image'])
                posted_records_hashes.append(record_hash)
        if len(posted_records_hashes) > 100:
            del posted_records_hashes[0]
        sleep(15)
