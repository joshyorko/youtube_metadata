from pydantic import BaseModel

class VideoMetadata(BaseModel):
    title: str
    description: str
    tags: list[str]