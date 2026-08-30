# ============================================================
# BRI CONFIGURATION — edit this file to customize your briefing
# ============================================================

# RSS feed sources — add or remove feeds here
# To add: paste a new feed URL inside quotes, followed by a comma
# To remove: delete the line or put a # at the start to disable it
RSS_FEEDS = [
    # News
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "https://venturebeat.com/category/ai/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.technologyreview.com/feed/",
    "https://news.ycombinator.com/rss",
    # Newsletters
    "https://importai.substack.com/feed",
    "https://www.deeplearning.ai/the-batch/feed/",
    "https://bensbites.beehiiv.com/feed",
    "https://tldr.tech/ai/rss",
    "https://www.oneusefulthing.org/feed",
    "https://simonwillison.net/atom/everything/",
    # Podcasts (show notes only)
    "https://www.latent.space/feed",
    "https://feeds.buzzsprout.com/2057836.rss",
    "https://changelog.com/practicalai/feed",
    "https://feeds.simplecast.com/no_priors",
    "https://www.dwarkeshpatel.com/feed",
    # Labs / Primary Sources
    "https://www.anthropic.com/rss.xml",
    "https://openai.com/blog/rss.xml",
    "https://deepmind.google/blog/rss.xml",
]

# How many hours back to look for articles (change to 48 for weekly newsletters)
LOOKBACK_HOURS = 24

# Maximum number of articles to pass to Claude
MAX_ARTICLES = 30

# Target briefing length in minutes — change this to make it shorter or longer
TARGET_LENGTH_MINUTES = 10

# Claude model — haiku is fast and cheap; change to "claude-sonnet-5" for higher quality
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# Maximum tokens for Claude's response (controls cost and length)
MAX_TOKENS = 4000
