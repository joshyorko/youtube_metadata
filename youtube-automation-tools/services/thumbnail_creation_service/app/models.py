from pydantic import BaseModel, Field
from typing import List, Optional

class ThumbnailRequest(BaseModel):
    description: str



class ImageData(BaseModel):
    b64_json: Optional[str] = None
    revised_prompt: Optional[str] = None
    url: str

class ThumbnailResponse(BaseModel):
    created: int
    data: List[ImageData]
