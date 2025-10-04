from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Video Downloader Backend is Running!"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Output file path
        ydl_opts = {
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "format": "best",
            "extractor_args": {"generic": ["impersonate=chrome"]},  # 👈 this is the key fix
        }

        os.makedirs("downloads", exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
