import requests
import json
import config


def get_last_wall_record(group_id):
    url = 'https://api.vk.com/method/wall.get'
    parameters = {'owner_id': group_id,
                  'access_token': config.vk_token,
                  'count': 2}
    r = requests.get(url, params=parameters).text
    response_json = json.loads(r)
    if 'is_pinned' in response_json['response'][1]:
        last_record = response_json['response'][2]
    else:
        last_record = response_json['response'][1]
    return last_record


def get_data_from_record(record):
    result = dict()
    result['text'] = record['text']
    result['id'] = record['id']
    if 'photo' in record['attachment']:
        result['image'] = record['attachment']['photo']['src_big']
    return result


def get_data_from_last_wall_record(group_id):
    return get_data_from_record(get_last_wall_record(group_id))
