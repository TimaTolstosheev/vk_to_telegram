import requests
import json
import config


def get_last_wall_record(group_id):
    url = 'https://api.vk.com/method/wall.get'
    parameters = {'owner_id': group_id,
                  'access_token': config.vk_token,
                  'count': 2,
                  'version': 5.73}
    r = requests.get(url, params=parameters).text
    response_json = json.loads(r)
    if 'is_pinned' in response_json['response'][1]:
        last_record = response_json['response'][2]
    else:
        last_record = response_json['response'][1]
    return last_record


def get_data_from_record(record):
    result = dict()
    attachments=list()
    result['text'] = record['text']
    try:
        for attachment in record['attachments']:
            if attachment['type'] == 'photo':
               attachments.append(attachment['photo']['src_big'])

        result['images']=attachments
    except KeyError:
        pass
    return result


def get_data_from_last_wall_record(group_id):
    return get_data_from_record(get_last_wall_record(group_id))
