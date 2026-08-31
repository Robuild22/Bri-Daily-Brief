import datetime


def build_page(script, audio_path="audio/brief.mp3"):
    today = datetime.date.today().strftime("%B %d, %Y")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Bri — Daily AI Brief</title>
  <style>
    body {{
      font-family: Georgia, serif;
      max-width: 760px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
      background: #fafaf8;
      color: #1a1a1a;
      line-height: 1.7;
    }}
    h1 {{ font-size: 2rem; margin-bottom: 0.25rem; }}
    .date {{ color: #666; margin-bottom: 2rem; font-style: italic; }}
    .player-section {{
      background: #fff;
      border: 1px solid #e0e0e0;
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 2rem;
    }}
    audio {{ width: 100%; margin-bottom: 1rem; }}
    .speed-controls {{ display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }}
    .speed-controls span {{ font-size: 0.9rem; color: #555; margin-right: 0.25rem; }}
    .speed-btn {{
      padding: 0.3rem 0.7rem;
      border: 1px solid #ccc;
      border-radius: 6px;
      background: #f5f5f5;
      cursor: pointer;
      font-size: 0.85rem;
    }}
    .speed-btn.active {{ background: #1a1a1a; color: #fff; border-color: #1a1a1a; }}

    /* --------------------------------------------------------
       AVATAR VIDEO PLACEHOLDER
       When you have a talking-avatar video ready, replace the
       <div> below with a <video> or <iframe> tag pointing to
       your video file or embed URL. Remove this entire comment
       and the placeholder div, and drop your video element in.
    -------------------------------------------------------- */
    .avatar-placeholder {{
      background: #e8e8e8;
      border: 2px dashed #bbb;
      border-radius: 12px;
      height: 280px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: #888;
      margin-bottom: 2rem;
      font-size: 1rem;
    }}
    .avatar-placeholder .icon {{ font-size: 3rem; margin-bottom: 0.5rem; }}

    .transcript-section h2 {{ font-size: 1.3rem; border-bottom: 1px solid #ddd; padding-bottom: 0.5rem; }}
    .transcript {{ white-space: pre-wrap; font-size: 1rem; }}
  </style>
</head>
<body>

  <h1>Bri — Daily AI Brief</h1>
  <p class="date">{today}</p>

  <!-- AVATAR VIDEO PLACEHOLDER — replace this block with your video when ready -->
  <div class="avatar-placeholder">
    <div class="icon">🎙️</div>
    <div>Talking avatar video will appear here</div>
    <div style="font-size:0.8rem; margin-top:0.4rem;">Replace this div in build_page.py</div>
  </div>

  <div class="player-section">
    <audio id="player" controls preload="metadata">
      <source src="{audio_path}" type="audio/mpeg" />
      Your browser does not support the audio element.
    </audio>
    <div class="speed-controls">
      <span>Speed:</span>
      <button class="speed-btn" onclick="setSpeed(0.75)">0.75x</button>
      <button class="speed-btn active" onclick="setSpeed(1)">1x</button>
      <button class="speed-btn" onclick="setSpeed(1.25)">1.25x</button>
      <button class="speed-btn" onclick="setSpeed(1.5)">1.5x</button>
      <button class="speed-btn" onclick="setSpeed(1.75)">1.75x</button>
      <button class="speed-btn" onclick="setSpeed(2)">2x</button>
      <button class="speed-btn" onclick="setSpeed(3)">3x</button>
      <button class="speed-btn" onclick="setSpeed(5)">5x</button>
    </div>
  </div>

  <div class="transcript-section">
    <h2>Full Transcript</h2>
    <div class="transcript">{script}</div>
  </div>

  <script>
    const player = document.getElementById("player");
    function setSpeed(rate) {{
      player.playbackRate = rate;
      document.querySelectorAll(".speed-btn").forEach(b => b.classList.remove("active"));
      event.target.classList.add("active");
    }}
  </script>

</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Bri: Web page saved to index.html")
