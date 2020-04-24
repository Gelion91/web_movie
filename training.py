import csv

from web_movie import create_app, get_response

app = create_app()
with app.app_context():
    result = []
    with open('data.csv', 'r', encoding='utf-8') as file:
        fields = ['film_page', 'img', 'name', 'category', 'content']
        reader = csv.DictReader(file, delimiter=',')
        x = 0
        for row in reader:
            result.append(row)
        print(result)

        print(row['name'])
    with open('data_set.csv', 'w', encoding='utf-8') as f:
        fields = ['film_page', 'img', 'name', 'category', 'content', 'id']
        writer = csv.DictWriter(f, fields, delimiter=',')
        writer.writeheader()
        i = 0
        for row in result:
            try:
                row['id'] = get_response(row['name'])
                writer.writerow(row)
            except:
                row['id'] = None
                writer.writerow(row)
