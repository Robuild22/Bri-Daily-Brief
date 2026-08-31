import os
import sys
from fetch_feeds import fetch_all_feeds
from generate_script import generate_briefing_script
from tts import text_to_speech


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

    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script)
    print("\nBri: Script saved to script.txt")

    print("\nBri: Converting script to audio...")
    audio_path = text_to_speech(script)
    size_kb = os.path.getsize(audio_path) // 1024
    print(f"Bri: Audio saved to {audio_path} ({size_kb} KB)")


if __name__ == "__main__":
    main()
