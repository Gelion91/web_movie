import csv

result = []
with open('data_set.csv', 'r', encoding='utf-8') as file:
    fields = ['film_page', 'img', 'name', 'category', 'content', 'id']
    reader = csv.DictReader(file, delimiter=',')
    x = 0
    formated = []
    for row in reader:
        formated = []
        formated_row = row['category'].lower().split(',')
        for cat in formated_row:
            cat = cat.replace('фильмы', '').replace('2020', '').replace('2019', '').replace('2018', '').replace('hd', '').strip()
            if cat:
                formated.append(cat)
        row['category'] = ', '.join(formated)
        result.append(row)
    print(result)

with open('data_set_formated.csv', 'w', encoding='utf-8') as f:
    fields = ['film_page', 'img', 'name', 'category', 'content', 'id']
    writer = csv.DictWriter(f, fields, delimiter=',')
    writer.writeheader()
    i = 0
    for row in result:
        writer.writerow(row)
