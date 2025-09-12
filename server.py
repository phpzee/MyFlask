import os
from flask import Flask, render_template, request
from app import generate_tts, HINDI_SPEAKERS   # TTS module
from newsfetch import fetch_local_news         # News module

app = Flask(__name__)

# ---------------- Home page ----------------
@app.route("/")
def index():
    """
    Homepage with links to TTS and News
    Passes last_updated for display on homepage
    """
    try:
        _, last_updated = fetch_local_news()  # Get latest timestamp
    except:
        last_updated = None
    return render_template("index.html", last_updated=last_updated)

# ---------------- TTS page ----------------
@app.route("/tts", methods=["GET", "POST"])
def tts_route():
    audio_file = None
    text = ""
    speaker = "Standard Hindi"

    if request.method == "POST":
        text = request.form.get("text", "")
        speaker = request.form.get("speaker", "Standard Hindi")
        if text.strip():
            try:
                audio_file = generate_tts(text, speaker)
            except Exception as e:
                return render_template("app.html",
                                       error=f"TTS Error: {str(e)}",
                                       success=None,
                                       filename=None,
                                       speakers=HINDI_SPEAKERS)

    return render_template("app.html",
                           error=None,
                           success=None,
                           filename=audio_file,
                           speakers=HINDI_SPEAKERS,
                           text=text,
                           selected_speaker=speaker)

# ---------------- News page ----------------
@app.route("/news")
def news_route():
    try:
        articles, last_updated = fetch_local_news()   # list of dicts: title, summary, link
        return render_template("fetchLocalNews.html",
                               articles=articles,
                               last_updated=last_updated)
    except Exception as e:
        return f"<p>News Fetch Error: {str(e)}</p><a href='/'>Back</a>"

# ---------------- Run app ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
