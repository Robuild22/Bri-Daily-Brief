# ============================================================
# TTS MODULE — to swap voices, edit only this file
# ============================================================
# Current provider: Microsoft Edge TTS (free, no API key)
# To switch to ElevenLabs or another paid voice, replace the
# body of text_to_speech() with the new provider's code.
# Keep the function signature exactly as-is:
#   text_to_speech(script: str, output_path: str) -> str
# ============================================================

import asyncio
import os
import edge_tts

# Change this line to use a different voice
# Full list of voices: https://github.com/rany2/edge-tts#usage
VOICE = "en-US-AriaNeural"


async def _synthesize(text, output_path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)


def text_to_speech(script, output_path="audio/brief.mp3"):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    asyncio.run(_synthesize(script, output_path))
    return output_path
