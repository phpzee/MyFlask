import feedparser
from datetime import datetime, timedelta

# RSS feeds from famous and free news portals
feeds = [
    "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",      # Mumbai
    "https://www.ndtv.com/rss/ndtv-mumbai-news",                         # NDTV Mumbai
    "https://www.hindustantimes.com/rss/topnews/rssfeed.xml",            # HT top news
    "https://indianexpress.com/section/cities/mumbai/feed/",             # Indian Express Mumbai
    "https://www.bbc.com/hindi/india/rss.xml",                           # BBC Hindi India
    "https://www.freepressjournal.in/rss/section/mumbai",                # Free Press Journal Mumbai
    "https://www.localpress.in/rss/mumbai"                                # Example local portal (replace with real)
]

MAX_ITEMS = 30

def fetch_local_news():
    articles = []
    now = datetime.utcnow()
    one_day_ago = now - timedelta(days=1)

    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if 'published_parsed' in entry:
                    published = datetime(*entry.published_parsed[:6])
                else:
                    continue

                # Only last 24 hours
                if published < one_day_ago:
                    continue

                title = entry.get('title', '')
                summary = entry.get('summary', '')
                link = entry.get('link', '')

                # Priority: Malvani > Malad West > Mumbai
                priority = 0
                title_lower = (title + " " + summary).lower()
                if "malvani" in title_lower:
                    priority = 3
                elif "malad west" in title_lower:
                    priority = 2
                elif "mumbai" in title_lower:
                    priority = 1

                if priority > 0:
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'link': link,
                        'priority': priority,
                        'published': published
                    })

        except Exception as e:
            print("Feed error:", e)

    # Sort by priority (Malvani first)
    articles.sort(key=lambda x: x['priority'], reverse=True)
    return articles[:MAX_ITEMS], datetime.now().strftime("%d %b %Y %H:%M:%S")
