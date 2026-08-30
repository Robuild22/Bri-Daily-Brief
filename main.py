import sys
from fetch_feeds import fetch_all_feeds
from generate_script import generate_briefing_script


def main():
    print("Bri: Fetching RSS feeds...")
    articles = fetch_all_feeds()
    print(f"Bri: Found {len(articles)} articles from the last 24 hours.")

    if not articles:
        print("Bri: No articles found. Exiting.")
        sys.exit(1)

    print("Bri: Generating briefing script with Claude...")
    script = generate_briefing_script(articles)

    print("\n" + "=" * 60)
    print("TODAY'S BRI BRIEFING SCRIPT")
    print("=" * 60 + "\n")
    print(script)
    print("\n" + "=" * 60)

    # Save script to file so later steps can use it
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script)
    print("\nBri: Script saved to script.txt")


if __name__ == "__main__":
    main()
