# importing required packages
from os import abort
from flask import Flask, request, render_template,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from security import password_2
import joblib
visited=False
#For english news loading model and vector
model=joblib.load('model.sav')
vector=joblib.load('vector.sav')

#For Hindi News loading vector and model
model_hn=joblib.load('model_hn.sav')
vector_hn=joblib.load('vector_hn.sav')
# Creating Flask App
app = Flask(__name__) # app name given to procfile in heroku
# Configuring SQLALCHEMY and setting it to sqlite
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# Initializing SQLALCHEMY
db=SQLAlchemy(app)
# Admin Table in db.sqlite Database
class admin(db.Model):
    username=db.Column(db.String(20),primary_key=True,nullable=False)
    password=db.Column(db.String(20),nullable=False)
# Contact Us Table in db.sqlite Database
class contactus(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    email=db.Column(db.String(30),nullable=False)
    message=db.Column(db.String(1000),nullable=False)
    time=db.Column(db.DateTime,default=datetime.utcnow)
# Designing Backend for registration of admin
@app.route('/create',methods=['GET','POST'])
def register():
    if visited:
        if request.method=='POST':
            username=request.form['username']
            password_1=request.form['password']
            user = admin.query.filter_by(username=username).first()
            if user is not None:
                return render_template('create.html',result='false')
            if not password_2(password_1):
                return render_template('create.html',result='lesssecure',user_name=username)
            new=admin(username=username,password=password_1)
            db.session.add(new)
            db.session.commit()
            return render_template('create.html',result='true')
        else:
            return render_template('create.html')
    else:
        abort(404)
# Designing Backend for login of admin
@app.route("/admin",methods=["GET","POST"])
def admin2():
    global visited
    visited=False
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        user = admin.query.filter_by(username=username).first()
        if user is None:
            return render_template('admin.html',answer='None')
        elif user.password == password:
            all=contactus.query.all()
            visited=True
            return render_template('database.html',alluser=all)
        else:
            return render_template('admin.html',answer='None')
    else:
        return render_template('admin.html')
# Designing Backend for  hindi news prediction
@app.route("/prediction_hn",methods=['GET','POST'])
def pre_hn():
    global visited
    visited=False
    if request.method=="POST":
        news_hn=str(request.form['news_hn'])
        predict_hn=model_hn.predict(vector_hn.transform([news_hn]))
        return render_template('prediction_hn.html',prediction_text_hn=f"News is {predict_hn[0]}")
    else:
        return render_template('prediction_hn.html')
# Designing Backend for english news prediction
@app.route("/prediction_en",methods=['GET','POST'])
def pre_en():
    global visited
    visited=False
    if request.method == "POST":
        news_en= str(request.form["news_eng"])
        predict=model.predict(vector.transform([news_en]))
        return render_template('prediction_en.html',prediction_text_eng=f"News is {predict[0]}")
    else:
        return render_template('prediction_en.html')
# Designing Backend for storing value of feedback in database
@app.route("/contactus",methods=['GET','POST'])
def contact():
    global visited
    visited=False    
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        message=request.form['message']
        contact_us=contactus(name=name,email=email,message=message)
        db.session.add(contact_us)
        db.session.commit()
        return render_template('contactus.html',submit_text=f"Your Response has been Recorded")
    else:
        return render_template('contactus.html')
# Writing aboutus page accessing code 
@app.route("/aboutus")
def aboutus():
    global visited
    visited=False
    return render_template('aboutus.html')
# Writing hindi website page accessing code 
@app.route("/hindi")
def hindi():
    global visited
    visited=False
    return render_template('hindi.html')
# Writing index(home) page accessing code 
@app.route("/")
def home():
    global visited
    visited=False
    return render_template('index.html')
# Running the Main app
if __name__ == "__main__":
    app.run(debug=True)