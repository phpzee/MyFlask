import feedparser
from datetime import datetime, timedelta

# List of RSS feeds covering Mumbai / India
RSS_FEEDS = [
    "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms",  # TOI Mumbai
    "https://feeds.feedburner.com/FreePressJournalMumbai",       # FPJ Mumbai
    "https://www.ndtv.com/rss/ndtvnews-mumbai.xml",             # NDTV Mumbai
    "https://www.hindustantimes.com/rss/mumbai/rssfeed.xml",    # HT Mumbai
    "https://news.google.com/rss/search?q=Malad+West+Mumbai&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=Malvani+Mumbai&hl=en-IN&gl=IN&ceid=IN:en",
    "https://www.dnaindia.com/rss/mumbai.xml",                  # DNA Mumbai
    "https://www.mid-day.com/rss/mumbai.xml",                   # Mid-Day Mumbai
    "https://www.livemint.com/rss/news",                        # LiveMint (India)
    "https://www.thehindu.com/news/cities/mumbai/?service=rss"  # The Hindu Mumbai
]

# Keywords to filter news
KEYWORDS = ["Malvani", "Malad West", "Mumbai"]

def fetch_local_news(max_items=30):
    news_items = []
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)

    for feed_url in RSS_FEEDS:
        try:
            d = feedparser.parse(feed_url)
            for entry in d.entries:
                pub_date = None
                if 'published_parsed' in entry and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif 'updated_parsed' in entry and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])

                if pub_date and pub_date < yesterday:
                    continue  # skip news older than 24 hours

                content = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
                if any(k.lower() in content for k in KEYWORDS):
                    news_items.append({
                        "title": entry.get("title", "No title"),
                        "link": entry.get("link", ""),
                        "summary": entry.get("summary", ""),
                        "published": pub_date.strftime("%d %b %Y %H:%M:%S") if pub_date else "Unknown",
                        "source": feed_url
                    })
                if len(news_items) >= max_items:
                    break
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {e}")

    return news_items
