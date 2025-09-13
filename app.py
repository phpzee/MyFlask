from gtts import gTTS
from pathlib import Path
import os, time

# Save folder inside Flask project
BASE_FOLDER = Path("static/mp3Files")
os.makedirs(BASE_FOLDER, exist_ok=True)


HINDI_SPEAKERS = {
    "Standard Hindi": {"lang": "hi", "tld": "co.in"},
    "Female-ish Hindi": {"lang": "hi", "tld": "com"},
    "Hindi UK Accent": {"lang": "hi", "tld": "co.uk"},
    "Hindi Canadian": {"lang": "hi", "tld": "ca"},
    "Hindi Australian": {"lang": "hi", "tld": "com.au"},
    "Hindi US Accent": {"lang": "hi", "tld": "us"},
    "Hindi Indian Regional": {"lang": "hi", "tld": "in"},
    "Hindi Standard 2": {"lang": "hi", "tld": "co.in"},
    "Hindi Female 2": {"lang": "hi", "tld": "co.in"},
    "Hindi Neutral": {"lang": "hi", "tld": "com"}
}

def generate_tts(text: str, speaker: str = "Standard Hindi") -> str:
    """
    Generate TTS ok audio and return relative path for Flask.
    """
    if speaker not in HINDI_SPEAKERS:
        speaker = "Standard Hindi"

    lang = HINDI_SPEAKERS[speaker]["lang"]
    tld = HINDI_SPEAKERS[speaker]["tld"]

    filename = f"tts_{int(time.time())}.mp3"
    file_path = BASE_FOLDER / filename

    tts = gTTS(text=text, lang=lang, tld=tld)
    tts.save(file_path)

    # Return relative path for Flask static serving
    return f"mp3Files/{filename}"

