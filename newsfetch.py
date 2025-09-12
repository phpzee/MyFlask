import feedparser

def fetch_local_news(max_items=30):
    feeds = [
        "https://rss.cnn.com/rss/edition.rss",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
    ]
    articles = []
    count = 0
    for url in feeds:
        try:
            d = feedparser.parse(url)
            for entry in d.entries:
                if count >= max_items:
                    break
                articles.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", "")
                })
                count += 1
        except:
            pass
    return articles
