from flask import Flask, render_template, redirect
from app import app as tts_app  # existing TTS Flask app
from newsfetch import fetch_local_news

app = Flask(__name__)  # Rename Flask instance to app for Render Procfile

# Home page with links
@app.route("/")
def home():
    return render_template("index.html")

# Route for TTS (existing app.py)
@app.route("/tts")
def tts_page():
    return redirect("/app")  # redirect to existing TTS route

# Route for Local News
@app.route("/news")
def news_page():
    news = fetch_local_news()
    return render_template("fetchLocalNews.html", news_list=news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
