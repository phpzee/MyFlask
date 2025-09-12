# newsfetch.py
import feedparser
from datetime import datetime, timedelta

# RSS feeds prioritized: Malvani → Malad West → Mumbai (free portals)
RSS_FEEDS = [
    "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",  # Mumbai / local
    "https://www.hindustantimes.com/rss/mumbai/rssfeed.xml",
    "https://www.freepressjournal.in/rss/mumbai"  # example free journal
]

MAX_ARTICLES = 20  # latest 20 articles

def fetch_local_news():
    """
    Fetch latest local news from RSS feeds for last 24 hours.
    Returns:
        articles: list of dicts {title, summary, link}
        last_updated: str
    """
    articles = []
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Parse published date
                if hasattr(entry, 'published_parsed'):
                    published = datetime(*entry.published_parsed[:6])
                    if published < yesterday:
                        continue  # skip older than 24h

                title = getattr(entry, 'title', 'No Title')
                summary = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
                link = getattr(entry, 'link', '#')
                articles.append({
                    "title": title,
                    "summary": summary,
                    "link": link
                })

                if len(articles) >= MAX_ARTICLES:
                    break
            if len(articles) >= MAX_ARTICLES:
                break
        except Exception as e:
            print("Feed error:", e)

    last_updated = datetime.now().strftime("%d %b %Y %H:%M:%S")
    return articles, last_updated
