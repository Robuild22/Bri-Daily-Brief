import datetime

# Plain string template — no f-string, so CSS curly braces need no escaping.
# The three BRI_*_PLACEHOLDER tokens are swapped in at the bottom.
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Bri — Daily AI Brief</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Inter', sans-serif;
      background: #050510;
      color: #e0e8ff;
      min-height: 100vh;
      background-image:
        linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
      background-size: 40px 40px;
    }

    .container {
      max-width: 780px;
      margin: 0 auto;
      padding: 3rem 1.5rem 4rem;
    }

    .header { text-align: center; margin-bottom: 2.5rem; }

    .logo {
      font-family: 'Orbitron', monospace;
      font-size: 3.5rem;
      font-weight: 900;
      background: linear-gradient(135deg, #00d4ff, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      letter-spacing: 0.12em;
    }

    .tagline {
      font-family: 'Orbitron', monospace;
      font-size: 0.7rem;
      letter-spacing: 0.3em;
      color: #00d4ff;
      text-transform: uppercase;
      margin-top: 0.4rem;
      opacity: 0.75;
    }

    .date {
      font-size: 0.9rem;
      color: #6b7db3;
      margin-top: 0.75rem;
      letter-spacing: 0.05em;
    }

    .divider {
      height: 1px;
      background: linear-gradient(90deg, transparent, #00d4ff, #a855f7, transparent);
