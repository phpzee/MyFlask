from flask import Flask, render_template, redirect, url_for
from app import app as tts_app  # TTS Flask app
from newsfetch import fetch_local_news
from pathlib import Path
import os

# Main server app
app = Flask(__name__)

# Folder for MP3 files
BASE_FOLDER = Path("mp3Files")
os.makedirs(BASE_FOLDER, exist_ok=True)

# Home page with links
@app.route("/")
def home():
    return render_template("index.html")  # links to /tts and /news

# TTS route
@app.route("/tts")
def tts_page():
    return redirect("/app")  # redirects to your TTS app.py route

# News route
@app.route("/news")
def news_page():
    news_list = fetch_local_news()
    return render_template("fetchLocalNews.html", news_list=news_list)

# Serve MP3 files if needed
@app.route("/mp3/<filename>")
def serve_mp3(filename):
    file_path = BASE_FOLDER / filename
    if file_path.exists():
        return tts_app.send_file(file_path, mimetype="audio/mpeg")
    else:
        return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
