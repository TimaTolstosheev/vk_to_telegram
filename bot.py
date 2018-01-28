import config

from time import sleep
from requests import get
from vk_wall_listener import get_data_from_last_wall_record


def send_message(message_text):
    url = 'https://api.telegram.org/bot' + config.telegram_token + '/sendMessage'
    parameters = {'chat_id': config.chat_id,
                  'text': message_text,
                  # 'parse_mode': 'HTML',
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
    last_posted_record_ids = dict()
    posted_reposts = dict()
    for group in config.vk_group_ids:
        last_posted_record_ids[group] = 0
    while True:
        for group in config.vk_group_ids:
            wall_record_data = get_data_from_last_wall_record(group)
            if wall_record_data['id'] > last_posted_record_ids[group]:
                if 'repost_id' in wall_record_data:
                    if wall_record_data['repost_id'] in posted_reposts and \
                            posted_reposts[wall_record_data['repost_id']] == wall_record_data['repost_owner_id']:
                        continue
                    else:
                        posted_reposts[wall_record_data['repost_id']] = wall_record_data['repost_owner_id']
                send_message(wall_record_data['text'])
                if 'image' in wall_record_data:
                    send_image(wall_record_data['image'])
                last_posted_record_ids[group] = wall_record_data['id']
        sleep(30)
