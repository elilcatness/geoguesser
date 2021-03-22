import os

import requests
from io import BytesIO

from scale_selection import get_toponym_scale


def get_image_of_city(city: str, img_type: str):
    geocode_url = 'http://geocode-maps.yandex.ru/1.x/'
    geocode_error_msg = 'Не удалось найти этот город на карте'
    static_url = 'http://static-maps.yandex.ru/1.x/'
    static_error_msg = 'Не удалось получить изображение города на карте'
    apikey = os.getenv('GEOCODE_APIKEY')

    geocode_response = requests.get(geocode_url, params={'geocode': city,
                                                         'format': 'json',
                                                         'results': 1,
                                                         'apikey': apikey})
    if geocode_response.status_code != 200:
        return geocode_error_msg
    results = geocode_response.json()['response']['GeoObjectCollection']['featureMember']
    if not results:
        return geocode_error_msg
    toponym = results[0]['GeoObject']
    coords = ','.join(toponym['Point']['pos'].split())
    size = ','.join(map(str, get_toponym_scale(toponym)))

    static_response = requests.get(static_url, params={'ll': coords,
                                                       'l': img_type,
                                                       'spn': size})
    return (static_error_msg if static_response.status_code != 200
            else BytesIO(static_response.content))
