from flask import Flask, request, send_file, jsonify, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # create a unique temp filename
        temp_id = str(uuid.uuid4())
        output_path = f"/tmp/{temp_id}.mp4"

        ydl_opts = {
            "outtmpl": output_path,
            "format": "best",
            "quiet": True,
        }

        # download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # send file to user
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        # cleanup after sending
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
        except Exception as cleanup_err:
            print(f"Cleanup error: {cleanup_err}")


if __name__ == "__main__":
    # only used when testing locally
    app.run(host="0.0.0.0", port=8000)
