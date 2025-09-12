from flask import Flask, render_template, request
from app import generate_tts       # import TTS functions
from newsfetch import fetch_local_news  # import News functions

app = Flask(__name__)

# ----- Home page -----
@app.route("/")
def index():
    return render_template("index.html")  # template with 2 links

# ----- TTS route -----
@app.route("/tts", methods=["GET", "POST"])
def tts_route():
    if request.method == "POST":
        text = request.form["text"]
        filename = generate_tts(text)
        return render_template("app.html", audio_file=filename, text=text)
    return render_template("app.html")

# ----- News route -----
@app.route("/news")
def news_route():
    articles = fetch_local_news()
    return render_template("fetchLocalNews.html", articles=articles)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
