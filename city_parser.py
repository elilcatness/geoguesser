import requests
from bs4 import BeautifulSoup
from random import shuffle


def parse_cities():
    url = 'https://33tura.ru/strany'
    response = requests.get(url)
    if not response:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find('table').find('tbody').find_all('tr')[2:]
    cities = list(filter(lambda x: x, [x[4] for x in map(lambda y: y.get_text().split('\n'), rows)]))
    shuffle(cities)
    return cities[:10]