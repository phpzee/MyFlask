# newsfetch.py
import feedparser
import bleach

FEEDS = [
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
]

MAX_ITEMS = 30

# allowed tags/attributes for summaries
ALLOWED_TAGS = ['p', 'br', 'a', 'img', 'b', 'i', 'strong', 'em', 'ul', 'li']
ALLOWED_ATTRS = {
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'style', 'height', 'width']
}
ALLOWED_PROTOCOLS = ['http', 'https']

def clean_html(html_text: str) -> str:
    if not html_text:
        return ""
    return bleach.clean(html_text,
                        tags=ALLOWED_TAGS,
                        attributes=ALLOWED_ATTRS,
                        protocols=ALLOWED_PROTOCOLS,
                        strip=True)

def fetch_local_news(max_items: int = MAX_ITEMS):
    articles = []
    count = 0
    for url in FEEDS:
        try:
            d = feedparser.parse(url)
            for entry in d.entries:
                if count >= max_items:
                    break
                title = entry.get('title', 'No title')
                summary_raw = entry.get('summary', '') or entry.get('description', '')
                summary = clean_html(summary_raw)
                link = entry.get('link', '')
                articles.append({'title': title, 'summary': summary, 'link': link})
                count += 1
        except Exception as e:
            # skip failed feed but continue others
            print("Feed error:", e)
    if not articles:
        articles = [{'title': 'No news found', 'summary': '', 'link': ''}]
    return articles
