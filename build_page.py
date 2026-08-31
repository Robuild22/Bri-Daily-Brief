import datetime


def build_page(script, audio_path="audio/brief.mp3"):
    today = datetime.date.today().strftime("%B %d, %Y")

    with open("template.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("BRI_DATE_PLACEHOLDER", today)
    html = html.replace("BRI_AUDIO_PLACEHOLDER", audio_path)
    html = html.replace("BRI_SCRIPT_PLACEHOLDER", script)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Bri: Web page saved to index.html")
