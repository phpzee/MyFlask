from flask import Flask, render_template, redirect, url_for
from app import app as tts_app  # existing TTS Flask app
from newsfetch import fetch_local_news  # updated news fetcher

server = Flask(__name__)

# Home page with links
@server.route("/")
def home():
    return render_template("index.html")  # links to TTS and News Fetch

# Route for TTS
@server.route("/tts")
def tts_page():
    # Redirect to the existing TTS app route
    return redirect("/app")  # /app should be your existing app.py route

# Route for news fetch
@server.route("/news")
def news_page():
    news = fetch_local_news()
    return render_template("fetchLocalNews.html", news_list=news)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)
