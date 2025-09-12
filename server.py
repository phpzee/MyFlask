from flask import Flask, render_template
from newsfetch import fetch_local_news

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>News Fetcher</h1><a href='/news'>Go to Local News</a>"

@app.route("/news")
def news():
    articles = fetch_local_news()
    return render_template("fetchLocalNews.html", articles=articles)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
