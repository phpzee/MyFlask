import feedparser
from datetime import datetime, timedelta
import time

# List of RSS feeds (Mumbai / India focused)
feeds = [
    "https://timesofindia.indiatimes.com/rssfeeds/2957162.cms",
    "https://feeds.feedburner.com/ndtvmumbai",
    "https://www.hindustantimes.com/rss/topnews/rssfeed.xml",
    "https://www.freepressjournal.in/rss/mumbai",
    "https://indianexpress.com/section/cities/mumbai/feed/",
    "https://www.cnn.com/rss/edition_india.rss",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
    "https://www.thehindu.com/news/cities/mumbai/?service=rss",
    "https://economictimes.indiatimes.com/rss.cms",
    "https://news.google.com/rss/search?q=malad+west+mumbai&hl=en-IN&gl=IN&ceid=IN:en"
]

# Keywords to filter location
keywords = ["Malvani", "Malad West", "Mumbai"]

def fetch_local_news():
    local_news = []
    now = datetime.utcnow()
    since = now - timedelta(hours=24)

    for url in feeds:
        try:
            d = feedparser.parse(url)
            for entry in d.entries:
                # Check published date if available
                pub_date = getattr(entry, "published_parsed", None)
                if pub_date:
                    pub_datetime = datetime.fromtimestamp(time.mktime(pub_date))
                    if pub_datetime < since:
                        continue  # skip older news

                # Filter by keywords
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                if any(k.lower() in (title + summary).lower() for k in keywords):
                    local_news.append({
                        "title": title,
                        "summary": summary,
                        "link": entry.get('link', ''),
                        "published": entry.get('published', '')
                    })
        except Exception as e:
            print("Error fetching feed:", url, e)
    return local_news
