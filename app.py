# app.py (TTS module)
from gtts import gTTS
from pathlib import Path
import os, time

# save mp3s to static/mp3Files so Flask can serve them via url_for('static', filename=...)
BASE_FOLDER = Path("static") / "mp3Files"
os.makedirs(BASE_FOLDER, exist_ok=True)

# Use only safe tlds known to work with gTTS; avoid 'in' and similar that caused 404
HINDI_SPEAKERS = {
    "Standard Hindi": {"lang": "hi", "tld": "com"},
    "Female-ish Hindi": {"lang": "hi", "tld": "com"},
    "Hindi UK Accent": {"lang": "hi", "tld": "co.uk"},
    "Hindi Canadian": {"lang": "hi", "tld": "ca"},
    "Hindi Australian": {"lang": "hi", "tld": "com.au"},
    "Hindi US Accent": {"lang": "hi", "tld": "us"},
    "Hindi Neutral": {"lang": "hi", "tld": "com"}
}

def generate_tts(text: str, speaker: str = "Standard Hindi") -> str:
    """
    Generate TTS audio from text and return static relative path
    e.g. "mp3Files/tts_12345.mp3"
    """
    if not text or not text.strip():
        raise Exception("Empty text for TTS")

    if speaker not in HINDI_SPEAKERS:
        speaker = "Standard Hindi"

    lang = HINDI_SPEAKERS[speaker]["lang"]
    tld = HINDI_SPEAKERS[speaker]["tld"]

    filename = f"tts_{int(time.time()*1000)}.mp3"
    file_path = BASE_FOLDER / filename

    # try with chosen tld; if fails, fallback to 'com'
    try:
        tts = gTTS(text=text, lang=lang, tld=tld)
        tts.save(file_path)
    except Exception as e:
        # fallback attempt with 'com'
        try:
            tts = gTTS(text=text, lang=lang, tld="com")
            tts.save(file_path)
        except Exception as e2:
            raise Exception(f"TTS generation failed: {e}; fallback failed: {e2}")

    # return path relative to static folder for url_for('static', filename=...)
    return f"mp3Files/{filename}"

if __name__ == "__main__":
    print("app.py is a module providing generate_tts(). Run server.py to serve the web UI.")
