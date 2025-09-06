from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL

app = FastAPI(title="TikTok API")

# Cho phép gọi từ frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # cho phép tất cả domain
    allow_methods=["*"],  # cho phép tất cả method (GET, POST,...)
    allow_headers=["*"],  # cho phép tất cả header
)

@app.get("/api/tiktok/{username}")
async def get_tiktok_videos(username: str):
    url = f"https://www.tiktok.com/@{username}"

    ydl_opts = {
        "quiet": True,                # không log chi tiết
        "skip_download": True,        # không tải video
        "extract_flat": True,         # chỉ lấy danh sách thô (nhanh hơn)
        "force_generic_extractor": False,  # chỉ dùng extractor TikTok, bỏ generic
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Nếu không có video
            if "entries" not in info:
                raise HTTPException(status_code=404, detail="No videos found")

            # Chỉ giữ thông tin cơ bản để API chạy nhanh
            videos = [
                {
                    "id": v.get("id"),
                    "channel": v.get("channel"),
                    "title": v.get("title"),
                    "url": v.get("url"),
                    "timestamp": v.get("timestamp"),
                }
                for v in info["entries"]
            ]

            return videos

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot fetch videos: {e}")
