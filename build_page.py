import datetime


def build_page(script, audio_path="audio/brief.mp3"):
    today = datetime.date.today().strftime("%B %d, %Y")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Bri — Daily AI Brief</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Inter', sans-serif;
      background: #050510;
      color: #e0e8ff;
      min-height: 100vh;
      background-image:
        linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
      background-size: 40px 40px;
    }}

    .container {{
      max-width: 780px;
      margin: 0 auto;
      padding: 3rem 1.5rem 4rem;
    }}

    .header {{ text-align: center; margin-bottom: 2.5rem; }}

    .logo {{
      font-family: 'Orbitron', monospace;
      font-size: 3.5rem;
      font-weight: 900;
      background: linear-gradient(135deg, #00d4ff, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      letter-spacing: 0.12em;
    }}

    .tagline {{
      font-family: 'Orbitron', monospace;
      font-size: 0.7rem;
      letter-spacing: 0.3em;
      color: #00d4ff;
      text-transform: uppercase;
      margin-top: 0.4rem;
      opacity: 0.75;
    }}

    .date {{
      font-size: 0.9rem;
      color: #6b7db3;
      margin-top: 0.75rem;
      letter-spacing: 0.05em;
    }}

    .divider {{
      height: 1px;
      background: linear-gradient(90deg, transparent, #00d4ff, #a855f7, transparent);
      margin: 2rem 0;
      opacity: 0.35;
    }}

    /* ============================================================
       EARTH VISUAL — rotating globe with mic overlay
       ============================================================
       TO REPLACE WITH YOUR AVATAR VIDEO when ready:
       1. Delete the entire <div class="earth-scene">...</div> block
       2. Paste your video in its place, for example:

          <video autoplay loop muted playsinline
                 style="width:100%;border-radius:16px;margin-bottom:2rem;">
            <source src="your-avatar.mp4" type="video/mp4" />
          </video>

       3. Remove the CSS below between the ==== markers
       ============================================================ */

    .earth-scene {{
      position: relative;
      height: 300px;
      border-radius: 16px;
      background: radial-gradient(ellipse at 50% 60%, #0a0a25 0%, #020208 100%);
      border: 1px solid rgba(0, 212, 255, 0.15);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      margin-bottom: 2rem;
    }}

    .earth-scene::before {{
      content: '';
      position: absolute;
      inset: 0;
      background-image:
        radial-gradient(1.5px 1.5px at 8% 12%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 18% 55%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 30% 20%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 45% 75%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 58% 10%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 68% 45%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 78% 80%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 88% 25%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 93% 60%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 5% 88%, rgba(255,255,255,0.4) 0%, transparent 100%);
    }}

    .earth-container {{
      position: relative;
      width: 170px;
      height: 170px;
    }}

    .atmosphere {{
      position: absolute;
      inset: -14px;
      border-radius: 50%;
      background: radial-gradient(circle at 38% 32%,
        transparent 48%,
        rgba(30, 144, 255, 0.18) 62%,
        rgba(0, 212, 255, 0.08) 75%,
        
