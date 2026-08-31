import datetime
import html


def build_page(script, audio_path="audio/brief.mp3"):
    today = datetime.date.today().strftime("%B %d, %Y")

    with open("template.html", "r", encoding="utf-8") as f:
        page = f.read()

    # Escape the script so stray < > & characters can't break the page
    safe_script = html.escape(script)

    page = page.replace("BRI_DATE_PLACEHOLDER", today)
    page = page.replace("BRI_AUDIO_PLACEHOLDER", audio_path)
    page = page.replace("BRI_SCRIPT_PLACEHOLDER", safe_script)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(page)
    print("Bri: Web page saved to index.html")
