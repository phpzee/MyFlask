# server.py
import os
from flask import Flask, render_template, request, url_for
from app import generate_tts, HINDI_SPEAKERS
from newsfetch import fetch_local_news

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tts", methods=["GET", "POST"])
def tts_route():
    audio_file = None
    error = None
    text = ""
    selected_speaker = "Standard Hindi"

    if request.method == "POST":
        text = request.form.get("text", "")
        selected_speaker = request.form.get("speaker", "Standard Hindi")
        if not text.strip():
            error = "Please enter some text"
        else:
            try:
                audio_file = generate_tts(text, selected_speaker)
            except Exception as e:
                error = str(e)

    # add a cache-busting timestamp to the audio URL in template via ts
    ts = int(os.times()[4]) if hasattr(os, "times") else None
    return render_template("app.html",
                           speakers=HINDI_SPEAKERS,
                           audio_file=audio_file,
                           text=text,
                           selected_speaker=selected_speaker,
                           error=error,
                           ts=ts)

@app.route("/news")
def news_route():
    try:
        articles = fetch_local_news()
        return render_template("fetchLocalNews.html", articles=articles)
    except Exception as e:
        return f"<p>News Fetch Error: {str(e)}</p><a href='/'>Back</a>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
