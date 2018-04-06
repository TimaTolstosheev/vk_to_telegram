import requests
import json
import config


def get_file_size_by_url(url):
    r = requests.head(url)
    return r.headers['Content-Length']    # запрашиваем только заголовок файла изображения и вытаскиваем из него объём файла


def calculate_hash_for_record(record):
    fields_to_hash = record['text']
    if 'images' in record:
        if len(record['images']) == 1:
            fields_to_hash += " "
            fields_to_hash += get_file_size_by_url(record['images'][0])
        elif len(record['images']) > 1:
            image_sizes = []
            for image_url in record['images']:
                image_sizes.append(get_file_size_by_url(image_url))
            image_sizes.sort()    # сортируем список размеров всех картинок, чтобы он выстроился в порядке возрастания размера
            for image_size in image_sizes:
                fields_to_hash += " "
                fields_to_hash += image_size
    return hash(repr(fields_to_hash))    # хешируем только текст поста + если есть, то добавляем к нему через пробел объём всех приложенных картинок в восходящем порядке

## chokingyou: всё, что выше, надо бы ещё дотестировать, именно пытаясь запостить ещё раз такой же текст с такой же парой фотографий, но в другом порядке — должен зарубать.


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
    pictures=list()
    videos=list()#list with links to all attached videos
    result['text'] = record['text']
    result['record_id'] = int(str(record['to_id']) + str(record['date']) + str(record['id'])) # извращение, но вроде только так можно именно линейно склеить три числа в одно, а не сложить математически
    if ('copy_owner_id' in record and 'copy_post_date' in record and 'copy_post_id' in record):
        result['original_record_id'] = int(str(record['copy_owner_id']) + str(record['copy_post_date']) + str(record['copy_post_id']))
    else:
        result['original_record_id'] = None    # задаю значение по умолчанию для не-репостов, чтобы всё было единообразно, и не приходилось проверять, а есть ли вообще такое поле у записи
    try:
        for attachment in record['attachments']:
            if attachment['type'] == 'photo':
               pictures.append(attachment['photo']['src_big'])
            if attachment['type'] == 'video':
               ownerID=str(attachment['video']['owner_id'])
               vid=str(attachment['video']['vid'])
               video_url='https://vk.com/video'+ownerID+'_'+vid #link to attached video
               videos.append(video_url)
        #чтобы зря не добавлять пустые списки с картинками и видео, проверяем на их длину
        if len(pictures)>0: result['images']=pictures
        if len(videos)>0: result['videos']=videos #new key with list of all video links
    except KeyError:
        pass
    result['hash'] = calculate_hash_for_record(result)    # формируем хеш и дописываем отдельным полем в словарь
    return result


def get_data_from_last_wall_record(group_id):
    return get_data_from_record(get_last_wall_record(group_id))
