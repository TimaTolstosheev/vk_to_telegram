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
    videos=list()#list with links to all attached videos
    result['text'] = record['text']
    try:
        for attachment in record['attachments']:
            if attachment['type'] == 'photo':
               attachments.append(attachment['photo']['src_big'])
            if attachment['type'] == 'video':
               ownerID=str(attachment['video']['owner_id'])
               vid=str(attachment['video']['vid'])
               video_url='https://vk.com/video'+ownerID+'_'+vid #link to attached video 
               videos.append(video_url)

        result['images']=attachments
        result['videos']=videos #new key with list of all video links
    except KeyError:
        pass
    return result


def get_data_from_last_wall_record(group_id):
    return get_data_from_record(get_last_wall_record(group_id))
