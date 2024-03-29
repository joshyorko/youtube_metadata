from fastapi import FastAPI, UploadFile, File
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Video(BaseModel):
    title: str
    description: str
    tags: List[str]

@app.post("/upload/")
async def upload_video(video: UploadFile = File(...), metadata: Video):
    # Here you would include the logic to upload the video to YouTube using YouTube's API
    # You would also use the metadata to set the video's title, description, and tags
    # This is a placeholder and the actual implementation will depend on the specific requirements and the YouTube API
    return {"filename": video.filename}