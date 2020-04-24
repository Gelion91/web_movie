from db import db
from web_movie import create_app

db.create_all(app=create_app())
