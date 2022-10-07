from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import joblib
#loading model
model=joblib.load('model.sav')
# TFIDF Vector Load
vector=joblib.load('vector.sav')

app = Flask(__name__) # app name given to procfile in heroku
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class admin(db.Model):
    username=db.Column(db.String(20),primary_key=True,nullable=False)
    password=db.Column(db.String(20),nullable=False)

class contactus(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    email=db.Column(db.String(30),nullable=False)
    message=db.Column(db.String(1000),nullable=False)
    time=db.Column(db.DateTime,default=datetime.utcnow)

@app.route('/create',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user = admin.query.filter_by(username=username).first()
        if user is not None:
            return render_template('create.html',result='false')
        new=admin(username=username,password=password)
        db.session.add(new)
        db.session.commit()
        return render_template('create.html',result='true')
    else:
        return render_template('create.html')

@app.route("/admin",methods=["GET","POST"])
def admin2():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        user = admin.query.filter_by(username=username).first()
        if user is None:
            return render_template('admin.html',answer='None')
        elif user.password == password:
            all=contactus.query.all()
            return render_template('database.html',alluser=all)
        else:
            return render_template('admin.html',answer='None')
    else:
        return render_template('admin.html')


@app.route("/prediction_hn")
def pre_hn():
    return render_template('prediction_hn.html')

@app.route("/prediction_en",methods=['GET','POST'])
def pre_en():
    if request.method == "POST":
        news_en= str(request.form["news_eng"])
        predict=model.predict(vector.transform([news_en]))
        return render_template('prediction_en.html',prediction_text_eng=f"News is {predict[0]}")
    else:
        return render_template('prediction_en.html')

@app.route("/contactus",methods=['GET','POST'])
def contact():
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

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@app.route("/hindi")
def hindi():
    return render_template('hindi.html')
    
@app.route("/")
def home():
    return render_template('index.html')
  
if __name__ == "__main__":
    app.run(debug=True)