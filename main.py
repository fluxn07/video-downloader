from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


@app.route("/")
def home():
    return "<h2>✅ Video Downloader Backend is Running!</h2>"


@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"error": "Missing URL"}), 400

        filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(DOWNLOADS_DIR, filename)

        # yt-dlp options
        ydl_opts = {
            "outtmpl": output_path,
            "format": "best",
            "quiet": True,
            "noplaylist": True,
            "extractor_args": {"generic": ["impersonate=chrome"]},  # Cloudflare bypass
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(output_path):
            return send_file(output_path, as_attachment=True)

        return jsonify({"error": "Failed to download file"}), 500

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
