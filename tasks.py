from celery import Celery
from celery.schedules import crontab

from web_movie import create_app
from web_movie.parse.get_id import get_film_id
from web_movie.parse.url_fasttorrent import scrap_filmlist, kino_scrap

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def content():
    with flask_app.app_context():
        for x in range(1, 10):
            scrap_filmlist(x)
        kino_scrap()
        get_film_id()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), content.s())