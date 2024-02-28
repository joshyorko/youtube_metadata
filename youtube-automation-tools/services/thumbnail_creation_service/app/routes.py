from fastapi import APIRouter
from .models import ThumbnailRequest, ThumbnailResponse
from .services.thumbnail import generate_thumbnail

router = APIRouter()

@router.post("/generate-thumbnail/", response_model=ThumbnailResponse)
async def create_thumbnail(request: ThumbnailRequest):
    return await generate_thumbnail(request.description)
