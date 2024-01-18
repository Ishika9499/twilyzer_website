from flask import Flask, render_template, request, redirect
app = Flask(__name__)
from analyze import SentimentAnalysisNLTK
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3
from matplotlib import style
import os

@app.route("/", methods=['GET', 'POST'])
def getquery():
    try:
        os.remove('static/images/figure1.png')  
    except Exception as e:
        print("Error : " + str(e))
    try:
        os.remove('static/images/figure2.png')  
    except Exception as e:
        print("Error : " + str(e)) 
    try:
        os.remove('static/images/figure3.png')  
    except Exception as e:
        print("Error : " + str(e)) 
    try:
        os.remove('static/images/figure5.png')
    except Exception as e:
        print("Error : " + str(e))
    obj1 = SentimentAnalysisNLTK()
    if request.method=='POST':
        query = request.form.get("keyword")
        obj1.fetch_tweets(query)
        return redirect("/Mainpage")
    return render_template("Opening_Page.html")

@app.route("/Sentiment")
def send_images_sentiment():
    return render_template("Sentiment.html", url1 = 'static/images/figure1.png', url2 = 'static/images/figure2.png')

@app.route("/Emotion")
def send_images_emotion():
    return render_template("Emotion.html", url1 = 'static/images/figure3.png')

@app.route("/Wordcloud")
def send_images_wordcloud():
    return render_template("Wordcloud.html", url1 = 'static/images/figure5.png')

@app.route("/Help")
def help():
    return render_template("Help.html")

@app.route("/Aboutus")
def aboutus():
    return render_template("About_Us.html")

@app.route("/Mainpage")
def mainpage():
    return render_template("Main_page.html")

@app.route("/Welcomepage")
def welcomepage():
    return render_template("Welcome_page.html")

if __name__=="__main__":
    app.run(debug=True)