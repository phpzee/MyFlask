from gtts import gTTS
from pathlib import Path
import os, time

# Save folder (inside project static folder for Flask)
BASE_FOLDER = Path("static/mp3Files")
os.makedirs(BASE_FOLDER, exist_ok=True)

# Hindi speakers (gTTS supports language + TLD trick for voice variations)
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
    Generate TTS audio from text.
    Returns the relative path to the MP3 file for Flask.
    """
    if speaker not in HINDI_SPEAKERS:
        speaker = "Standard Hindi"

    lang = HINDI_SPEAKERS[speaker]["lang"]
    tld = HINDI_SPEAKERS[speaker]["tld"]

    filename = f"tts_{int(time.time())}.mp3"
    file_path = BASE_FOLDER / filename

    try:
        tts = gTTS(text=text, lang=lang, tld=tld)
        tts.save(file_path)
        return f"mp3Files/{filename}"  # relative path for Flask static
    except Exception as e:
        raise Exception(f"TTS Error: {str(e)}")

# Optional: Keep standalone Flask app for local testing (like before)
if __name__ == "__main__":
    from flask import Flask, render_template, request, send_file

    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        error = None
        success = None
        filename = None

        if request.method == "POST":
            text = request.form.get("text", "")
            speaker = request.form.get("speaker", "Standard Hindi")
            if not text.strip():
                error = "Please enter some text!"
            else:
                try:
                    filename = generate_tts(text, speaker)
                    success = f"MP3 ready: {filename}"
                except Exception as e:
                    error = str(e)

        return render_template("app.html", error=error, success=success, filename=filename, speakers=HINDI_SPEAKERS)

    @app.route("/play/<filename>")
    def play_file(filename):
        file_path = BASE_FOLDER / filename
        return send_file(file_path, mimetype="audio/mpeg")

    @app.route("/download/<filename>")
    def download_file(filename):
        file_path = BASE_FOLDER / filename
        return send_file(file_path, as_attachment=True)

    app.run(host="0.0.0.0", port=5000, debug=True)
