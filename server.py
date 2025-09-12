import os
from flask import Flask, render_template, request
from app import generate_tts       # TTS functions from your existing app.py
from newsfetch import fetch_local_news  # News functions

app = Flask(__name__)

# ---------------- Home page ----------------
@app.route("/")
def index():
    return render_template("index.html")  # Homepage with links to TTS and News

# ---------------- TTS Route ----------------
@app.route("/tts", methods=["GET", "POST"])
def tts_route():
    if request.method == "POST":
        text = request.form.get("text", "")
        if text.strip() != "":
            try:
                filename = generate_tts(text)  # creates static/output.mp3
                return render_template("app.html", audio_file=filename, text=text)
            except Exception as e:
                return f"<p>TTS Error: {str(e)}</p><a href='/tts'>Back</a>"
    return render_template("app.html")

# ---------------- News Route ----------------
@app.route("/news")
def news_route():
    try:
        articles = fetch_local_news()
        return render_template("fetchLocalNews.html", articles=articles)
    except Exception as e:
        return f"<p>News Fetch Error: {str(e)}</p><a href='/'>Back</a>"

# ---------------- Run ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
