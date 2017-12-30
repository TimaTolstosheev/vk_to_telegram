import requests
import json
import config


def get_last_wall_record(group_id):
    url = 'https://api.vk.com/method/wall.get'
    parameters = {'owner_id': group_id,
                  'access_token': config.vk_token,
                  'count': 1}
    return requests.get(url, params=parameters).text


def get_data_from_response(response):
    data_dict = json.loads(response)
    text = data_dict['response'][1]['text']
    id = data_dict['response'][1]['id']
    if 'photo' in data_dict['response'][1]['attachment']:
        image_url = data_dict['response'][1]['attachment']['photo']['src_xxbig']
        return {'id': id, 'text': text, 'image': image_url}
    else:
        return {'id': id, 'text': text}


def get_data_from_last_wall_record(group_id):
    return get_data_from_response(get_last_wall_record(group_id))


if __name__ == '__main__':
    print(get_data_from_response(get_last_wall_record()))
