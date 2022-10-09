#importing from app.py db(sqlalchemy model) and app(flask app)
from app import db,app
# Creating Database db.sqlite and all the tables in it wriiten in app.py
with app.app_context():
    db.create_all()
