from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Metadata(BaseModel):
    title: str
    description: str
    tags: list[str]

@app.post("/metadata/")
async def create_metadata(metadata: Metadata):
    # TODO: Implement the logic to handle video metadata
    return {"message": "Metadata received"}

@app.get("/metadata/{video_id}")
async def read_metadata(video_id: str):
    # TODO: Implement the logic to retrieve and return video metadata
    return {"message": "Metadata for video_id"}