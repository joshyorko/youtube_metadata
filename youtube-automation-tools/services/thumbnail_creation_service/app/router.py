from fastapi import APIRouter
from .schemas import ThumbnailRequest, ThumbnailResponse
from .services.thumbnail import generate_thumbnail

router = APIRouter()

@router.post("/api/v1/generate-thumbnail/", response_model=ThumbnailResponse, tags=["Thumbnail"])
async def create_thumbnail(request: ThumbnailRequest):
    return await generate_thumbnail(request.description)
