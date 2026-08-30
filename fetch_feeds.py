import feedparser
import datetime
from config import RSS_FEEDS, LOOKBACK_HOURS, MAX_ARTICLES


def fetch_all_feeds():
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=LOOKBACK_HOURS)
    articles = []

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                pub = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub = datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    pub = datetime.datetime(*entry.updated_parsed[:6], tzinfo=datetime.timezone.utc)

                # Skip articles older than the cutoff; include articles with no date
                if pub and pub < cutoff:
                    continue

                title = entry.get("title", "").strip()
                summary = entry.get("summary", entry.get("description", "")).strip()
                source = feed.feed.get("title", url)

                if title:
                    articles.append({
                        "title": title,
                        "summary": summary[:800],
                        "source": source,
                        "published": pub.isoformat() if pub else "unknown",
                    })
        except Exception as e:
            print(f"Warning: skipping feed {url} — {e}")
            continue

    articles.sort(key=lambda a: a["published"], reverse=True)
    return articles[:MAX_ARTICLES]
