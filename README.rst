web_movie
====

Приложение для просмотра кино онлайн. 
Для запуска проекта на вашем компьютере вам понадобится Python3.6+.
приложение было написано на Flask

Установка
----

Создайте виртуальное окружение и активируйте его. Потом установите все необходимые зависимости:

..code-block:: text

    pip install -r requirements.txt

Зарегистрируйтесь на https://xml.yandex.ru и получите там данные USER и KEY, это понадобится для получения id фильма с www.kinopoisk.ru

Создайте в корне проекта файл config.py:

..code-block:: python

    import os
    from datetime import timedelta
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    
    USER = 'Ваш логин на yandex.xml'
    KEY = 'Ваш ключ на yandex.xml'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'web_movie.db') #место хранения базы данных
    SECRET_KEY = 'Введите сложный набор символов который будет служить CSRF'
    FILM_PER_PAGE = 15 #Количество фильмов на странице
    REMEMBER_COOKIE_DURATION = timedelta(days=1) #Срок хранения cookie
    

Создайте базу данных:

..code-block:: text

    python3 create_db.py
    
Создайте пользователя с правами администратора:

..code-block:: text

    python3 create_admin.py
    
Запуск
----

Запуск на Unix-подобных операционных системах:

..code-block:: text

    ./run.sh
    
Или

..code-block:: text

    python3 wsgi.py

