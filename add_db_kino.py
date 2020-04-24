import csv
from web_movie import create_app, db
from web_movie.video.models import Film

x = 0
app = create_app()
with app.app_context():
    with open('data_set_formated.csv', 'r', encoding='utf-8') as file:
        fields = ['film_page', 'img', 'name', 'category', 'content', 'id']
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            x += 1

            new_video = Film.query.filter(Film.kino_id == row['id']).count()
            if not new_video:
                print(f'{x} {row}')
                numbers = row['name'].split()[-1].replace('(', '').replace(')', '').strip()
                if numbers.isdigit():
                    year = numbers
                else:
                    year = '-'
                new_video = Film(
                    img=row['img'], name=row['name'].split('(')[0].strip().lower(),
                    category=row['category'], kino_id=row['id'],
                    content=row['content'], film_page=row['film_page'], year=year
                )
                db.session.add(new_video)
                db.session.commit()
