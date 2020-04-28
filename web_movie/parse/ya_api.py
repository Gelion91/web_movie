from flask import current_app
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import re


def get_response(query):
    url = 'https://yandex.com/search/xml'
    parameters = {
        'user': current_app.config['USER'],
        'key': current_app.config['KEY'],
        'query': query + ' кинопоиск',
    }
    session = Session()
    try:
        response = session.get(url, params=parameters)
        data = response.text
        start = re.search(r'/film/\w+/', data)
        start = start.group(0).split('/')
        print(start[-2])
        return start[-2]
    except (ConnectionError, Timeout, TooManyRedirects, AttributeError) as e:
        print(e)

