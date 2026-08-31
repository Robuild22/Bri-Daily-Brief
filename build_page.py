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

    /* --------------------------------------------------------
       AVATAR VIDEO PLACEHOLDER
       When your talking-avatar video is ready, delete the
       .avatar-placeholder div below and replace it with:

         <video autoplay loop muted playsinline
                style="width:100%; border-radius:16px;">
           <source src="your-avatar.mp4" type="video/mp4" />
         </video>

       For a hosted embed, use an <iframe> instead.
       Remove this comment block too.
    -------------------------------------------------------- */
    .avatar-placeholder {{
      position: relative;
      height: 300px;
      border-radius: 16px;
      background: linear-gradient(135deg, #0d0d2b, #0a1628);
      border: 1px solid rgba(0, 212, 255, 0.2);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      margin-bottom: 2rem;
    }}

    .avatar-placeholder::before {{
      content: '';
      position: absolute;
      width: 220px;
      height: 220px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(168,85,247,0.15), rgba(0,212,255,0.05), transparent 70%);
      animation: pulse 3s ease-in-out infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ transform: scale(1); opacity: 0.6; }}
      50% {{ transform: scale(1.15); opacity: 1; }}
    }}

    .avatar-ring {{
      width: 120px;
      height: 120px;
      border-radius: 50%;
      border: 2px solid rgba(0, 212, 255, 0.45);
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      margin-bottom: 1.2rem;
    }}

    .avatar-ring::after {{
      content: '';
      position: absolute;
      inset: -10px;
      border-radius: 50%;
      border: 1px solid rgba(168, 85, 247, 0.2);
    }}

    .avatar-icon {{ font-size: 3rem; }}

    .avatar-label {{
      font-family: 'Orbitron', monospace;
      font-size: 0.6rem;
      letter-spacing: 0.25em;
      color: #6b7db3;
      text-transform: uppercase;
      position: relative;
    }}

    .player-section {{
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(0, 212, 255, 0.15);
      border-radius: 16px;
      padding: 1.5rem;
      margin-bottom: 2rem;
    }}

    audio {{
      width: 100%;
      margin-bottom: 1.2rem;
      border-radius: 8px;
      accent-color: #00d4ff;
    }}

    .speed-label {{
      font-family: 'Orbitron', monospace;
      font-size: 0.6rem;
      letter-spacing: 0.2em;
      color: #6b7db3;
      text-transform: uppercase;
      margin-bottom: 0.6rem;
    }}

    .speed-controls {{ display: flex; gap: 0.4rem; flex-wrap: wrap; }}

    .speed-btn {{
      padding: 0.35rem 0.65rem;
      border: 1px solid rgba(0, 212, 255, 0.2);
      border-radius: 6px;
      background: transparent;
      color: #6b7db3;
      cursor: pointer;
      font-size: 0.8rem;
      font-family: 'Inter', sans-serif;
      transition: all 0.2s;
    }}

    .speed-btn:hover {{ border-color: rgba(0,212,255,0.5); color: #00d4ff; }}

    .speed-btn.active {{
      background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(168,85,247,0.15));
      border-color: #00d4ff;
      color: #00d4ff;
    }}

    .transcript-section {{
      border-top: 1px solid rgba(0, 212, 255, 0.1);
      padding-top: 2rem;
    }}

    .transcript-heading {{
      font-family: 'Orbitron', monospace;
      font-size: 0.65rem;
      letter-spacing: 0.3em;
      color: #00d4ff;
      text-transform: uppercase;
      margin-bottom: 1.5rem;
      opacity: 0.7;
    }}

    .transcript {{
      white-space: pre-wrap;
      font-size: 1rem;
      line-height: 1.85;
      color: #c0ccee;
      font-weight: 300;
    }}
  </style>
</head>
<body>
  <div class="container">

    <div class="header">
      <div class="logo">BRI</div>
      <div class="tagline">Daily AI Intelligence Brief</div>
      <div class="date">{today}</div>
    </div>

    <div class="divider"></div>

    <!-- AVATAR PLACEHOLDER — replace this div with your video element when ready -->
    <div class="avatar-placeholder">
      <div class="avatar-ring">
        <div class="avatar-icon">🎙️</div>
      </div>
      <div class="avatar-label">Avatar coming soon</div>
    </div>

    <div class="player-section">
      <audio id="player" controls preload="metadata">
        <source src="{audio_path}" type="audio/mpeg" />
        Your browser does not support the audio element.
      </audio>
      <div class="speed-label">Playback Speed</div>
      <div class="speed-controls">
        <button class="speed-btn" onclick="setSpeed(0.75, this)">0.75×</button>
        <button class="speed-btn active" onclick="setSpeed(1, this)">1×</button>
        <button class="speed-btn" onclick="setSpeed(1.25, this)">1.25×</button>
        <button class="speed-btn" onclick="setSpeed(1.5, this)">1.5×</button>
        <button class="speed-btn" onclick="setSpeed(1.75, this)">1.75×</button>
        <button class="speed-btn" onclick="setSpeed(2, this)">2×</button>
        <button class="speed-btn" onclick="setSpeed(2.5, this)">2.5×</button>
        <button class="speed-btn" onclick="setSpeed(3, this)">3×</button>
        <button class="speed-btn" onclick="setSpeed(4, this)">4×</button>
        <button class="speed-btn" onclick="setSpeed(5, this)">5×</button>
      </div>
    </div>

    <div class="transcript-section">
      <div class="transcript-heading">Full Transcript</div>
      <div class="transcript">{script}</div>
    </div>

  </div>

  <script>
    const player = document.getElementById("player");
    function setSpeed(rate, btn) {{
      player.playbackRate = rate;
      document.querySelectorAll(".speed-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
    }}
  </script>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Bri: Web page saved to index.html")
