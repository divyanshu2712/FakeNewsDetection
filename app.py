from flask import Flask, escape, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
#loading model
model=joblib.load('model.sav')
# TFIDF Vector Load
vector=joblib.load('vector.sav')

app = Flask(__name__)

@app.route("/prediction_hn.html")
def pre_hn():
    return render_template('prediction_hn.html')

@app.route("/prediction_en.html",methods=['GET','POST'])
def pre_en():
    if request.method == "POST":
        news_en= str(request.form["news_eng"])
        predict=model.predict(vector.transform([news_en]))
        return render_template('prediction_en.html',prediction_text_eng=f"News is {predict[0]}")
    else:
        return render_template('prediction_en.html')

@app.route("/contactus.html")
def contact():
    return render_template('contactus.html')

@app.route("/aboutus.html")
def aboutus():
    return render_template('aboutus.html')

@app.route("/hindi.html")
def hindi():
    return render_template('hindi.html')

@app.route("/index.html")
def home_1():
    return render_template('index.html')
    
@app.route("/")
def home():
    return render_template('index.html')
  
if __name__ == "__main__":
    app.run(debug=True)