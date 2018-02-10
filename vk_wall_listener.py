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
    result = dict()
    result['text'] = data_dict['response'][1]['text']
    result['id'] = data_dict['response'][1]['id']
    if 'photo' in data_dict['response'][1]['attachment']:
        result['image'] = data_dict['response'][1]['attachment']['photo']['src_big']
    return result


def get_data_from_last_wall_record(group_id):
    return get_data_from_response(get_last_wall_record(group_id))
