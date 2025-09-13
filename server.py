from flask import Flask, render_template
from app import app as tts_app  # Keep your existing TTS app intact
from newsfetch import fetch_local_news

app = Flask(__name__)

@app.route("/")
def home():
    # Simple home page with links to TTS and News
    return render_template("index.html")

@app.route("/tts", methods=["GET", "POST"])
def tts_page():
    # Call existing TTS Flask app route
    return tts_app.index()

@app.route("/news")
def news_page():
    # Fetch latest news and send to template
    news_list = fetch_local_news()
    return render_template("fetchLocalNews.html", news_list=news_list)
