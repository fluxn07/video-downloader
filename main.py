from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# ✅ Allow requests from any frontend (e.g. Render or Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL if you want security later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "✅ Video Downloader Backend is Running!"}

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    url = data.get("url")

    if not url:
        return {"error": "No URL provided"}

    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "format": "best",
            "noplaylist": True,
            "extract_flat": False,
            "outtmpl": "%(title)s.%(ext)s",
            "ignoreerrors": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Try to extract video URL safely
            video_url = info.get("url")
            if not video_url and "entries" in info and len(info["entries"]) > 0:
                video_url = info["entries"][0].get("url")

            if not video_url:
                return {"error": "Unable to extract video URL. Might require login or cookies."}

            return {
                "title": info.get("title", "Unknown title"),
                "thumbnail": info.get("thumbnail", ""),
                "video_url": video_url,
                "duration": info.get("duration", 0),
                "source": info.get("extractor", "unknown"),
            }

    except Exception as e:
        return {"error": str(e)}
