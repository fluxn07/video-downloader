from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "✅ Video Downloader Backend is Running!"}

@app.post("/download")
async def download_video(request: Request):
    try:
        data = await request.json()
        url = data.get("url")

        if not url:
            return {"error": "No URL provided"}

        ydl_opts = {
            "quiet": True,
            "format": "best",
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "url": info.get("url")
            }
    except Exception as e:
        return {"error": str(e)}

