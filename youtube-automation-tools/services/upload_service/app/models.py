from pydantic import BaseModel

class UploadVideo(BaseModel):
    title: str
    description: str
    tags: list[str]
    video_file: bytes