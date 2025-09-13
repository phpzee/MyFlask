from flask import Flask, render_template, redirect, url_for
from app import app as tts_app  # Import your existing TTS Flask app
from newsfetch import fetch_local_news
from pathlib import Path
import os

# Main server app
app = Flask(__name__)

# Ensure mp3 folder exists for TTS files
BASE_FOLDER = Path("mp3Files")
os.makedirs(BASE_FOLDER, exist_ok=True)

# Home page with links to TTS and News Fetch
@app.route("/")
def home():
    return render_template("index.html")  # index.html has links to /tts and /news

# Route to TTS app
@app.route("/tts")
def tts_page():
    return redirect("/app")  # redirect to TTS app route in app.py

# Route to fetch and display local news
@app.route("/news")
def news_page():
    news_list = fetch_local_news()
    return render_template("fetchLocalNews.html", news_list=news_list)

# Optional: serve MP3 files if needed
@app.route("/mp3/<filename>")
def serve_mp3(filename):
    file_path = BASE_FOLDER / filename
    if file_path.exists():
        return tts_app.send_file(file_path, mimetype="audio/mpeg")
    else:
        return "File not found", 404

if __name__ == "__main__":
    # For local testing only; Render uses Gunicorn via Procfile
    app.run(host="0.0.0.0", port=5000, debug=True)
