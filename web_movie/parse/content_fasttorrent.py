import csv
from bs4 import BeautifulSoup
from web_movie.parse.url_fasttorrent import get_html


def kino_scrap(name, x):
    """Парсинг данных со страницы фильма и сохранение в csv формате"""
    year, category, country, producer, actors, operator, music_author, content, img = '', '', '', '', '', '', '', '', ''
    html = get_html(f'http://fast-torrent.ru{x}')
    if html:
        try:
            soup = BeautifulSoup(html, 'html.parser')
            content_films = soup.find('td', class_="info").find('div')
            year = soup.find('p', class_='').text
            category = soup.find_all('p')[1].text

            country = []
            for i in content_films('a'):
                if i.find('em', class_='cn-icon'):
                    country.append(i.find('em', class_='cn-icon')['title'])

            for prod in content_films('p', align='left'):
                if "Режиссер" in prod.find('strong'):
                    producer = prod.find('a').text
                elif "В ролях" in prod.find('strong'):
                    actors = []
                    for i in prod.find_all('a'):
                        actors.append(i.text)
                elif "Оператор" in prod.find('strong'):
                    operator = prod.find('a').text
                elif "Композитор" in prod.find('strong'):
                    music_author = prod.find('a').text

            content = content_films.find('p', class_='justify').text
            img = soup.find('a', class_='slideshow1')['href']
            result = {'name': name, 'year': year, 'category': category,
                      'country': country, 'producer': producer, 'actors': actors,
                      'operator': operator, 'music_author': music_author, 'content': content, 'img': img}
            return result
        except:
            print('Ошибка')


def save_film(result):
    fields = ['name', 'year', 'category', 'country', 'producer', 'actors', 'operator', 'music_author',
              'content', 'img']
    with open('content_fasttorrent.csv', 'a+', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fields, delimiter=',', lineterminator='\n')
        writer.writeheader()
        try:
            writer.writerow(result)
            print('success')
        except:
            print('oops')


if __name__ == '__main__':
    with open('url_fasttorrent.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',')
        x = 0
        for row in reader:
            x += 1
            print(x)
            save_film(kino_scrap(row['name'], row['url']))
