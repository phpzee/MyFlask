import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Define news sources (RSS or website URLs)
NEWS_SOURCES = {
    "Times of India": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    "Google News India": "https://news.google.com/rss/search?q=Malad+West+Mumbai&hl=en-IN&gl=IN&ceid=IN:en",
    "Free Press Journal": "https://www.freepressjournal.in/rss",
    # Add more RSS feeds as needed
}

# Filter: last 24 hours
TIME_DELTA = timedelta(hours=24)

def fetch_local_news():
    all_news = []

    for source_name, url in NEWS_SOURCES.items():
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")  # RSS is XML
            items = soup.find_all("item")

            for item in items:
                title = item.title.text if item.title else "No title"
                link = item.link.text if item.link else "#"
                pub_date_text = item.pubDate.text if item.pubDate else None

                # Convert pubDate to datetime object
                if pub_date_text:
                    try:
                        pub_date = datetime.strptime(pub_date_text, "%a, %d %b %Y %H:%M:%S %Z")
                    except Exception:
                        pub_date = datetime.now()  # fallback
                else:
                    pub_date = datetime.now()

                # Check if published within last 24 hours
                if datetime.now() - pub_date <= TIME_DELTA:
                    # Check if title/location contains "Malvani" or "Malad"
                    if any(loc in title for loc in ["Malvani", "Malad", "Mumbai"]):
                        all_news.append({
                            "source": source_name,
                            "title": title,
                            "link": link,
                            "pub_date": pub_date.strftime("%d %b %Y %H:%M")
                        })

        except Exception as e:
            print(f"Error fetching {source_name}: {e}")

    # Sort news by pub_date descending
    all_news.sort(key=lambda x: x["pub_date"], reverse=True)
    return all_news
