# This program is used only to add the first admin  
# importing from app the table admin and db,app(flask application)
from app import admin,app,db
# Taking Input of Username and Password
user=input("Enter User name: ")
pass_word=input("Enter Password: ")
#Adding the given password and username to admin table
with app.app_context():
    admin1=admin(username=user,password=pass_word)
    db.session.add(admin1)
    db.session.commit()
