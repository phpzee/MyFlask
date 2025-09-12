import feedparser
from datetime import datetime, timedelta
import pytz
import re

# ---------------- RSS feeds ----------------
feeds = [
    "https://news.google.com/rss/search?q=Malvani+Mumbai&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=Malad+West+Mumbai&hl=en-IN&gl=IN&ceid=IN:en",
    "https://www.freepressjournal.in/rss/mumbai",
    "https://www.hindustantimes.com/rss/mumbai/rssfeed.xml",
    "https://www.mid-day.com/rss/mumbai.xml",
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.bbci.co.uk/news/world/rss.xml"
]

MAX_ITEMS = 50  # maximum articles to fetch

# ---------------- Utility ----------------
def extract_image(entry):
    """Try to get image URL from entry, else None"""
    # Google News uses media:thumbnail
    if 'media_content' in entry and entry.media_content:
        return entry.media_content[0].get('url')
    # Check for img tags in summary
    match = re.search(r'<img.*?src="(.*?)"', entry.get('summary', ''))
    if match:
        return match.group(1)
    return None

def clean_summary(summary):
    """Remove HTML tags from summary"""
    clean = re.sub('<.*?>', '', summary)
    return clean.strip()

# ---------------- Fetch function ----------------
def fetch_local_news():
    articles = []
    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    last_24h = now - timedelta(hours=24)

    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6], tzinfo=pytz.timezone("Asia/Kolkata"))
                
                # skip older than 24 hours
                if published and published < last_24h:
                    continue

                title = entry.get("title", "No title")
                summary = clean_summary(entry.get("summary", ""))
                link = entry.get("link", "")
                image = extract_image(entry)

                # prioritize Malvani > Malad West > Mumbai
                priority = 0
                if "Malvani" in title or "Malvani" in summary:
                    priority = 3
                elif "Malad West" in title or "Malad West" in summary:
                    priority = 2
                elif "Mumbai" in title or "Mumbai" in summary:
                    priority = 1

                articles.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "image": image,
                    "priority": priority
                })

        except Exception as e:
            print(f"Feed error ({url}): {e}")

    # sort by priority then title
    articles = sorted(articles, key=lambda x: (-x["priority"], x["title"]))
    return articles[:MAX_ITEMS]
