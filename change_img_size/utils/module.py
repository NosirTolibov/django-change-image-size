""" Модуль содержит функции"""
import mimetypes
import requests


def is_url_image(url):
    """
    Проверка url на наличие файла изображении

    :param url:
    :return: True/False/None
    """
    mimetype, encoding = mimetypes.guess_type(url)
    return mimetype and mimetype.startswith('image')


def check_url_status(url):
    """
    Проверка http статус url

    :param url:
    :return:
    """
    headers = {
        "User-Agent": "MyAppAgent/1.0",
        "Accept": "*/*"
    }
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions as e:
        return False
    return response.status_code in range(200, 209)
