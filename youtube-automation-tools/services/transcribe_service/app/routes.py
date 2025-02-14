from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from .services.transcribe import transcribe_audio_file, transcribe_youtube_video
from .models import TranscriptionResult
from .auth import get_current_user  # Fixed relative import

transcribe_router = APIRouter()

@transcribe_router.post("/", response_model=TranscriptionResult)
async def transcribe_route(
    file: UploadFile = File(None),
    youtube_url: str = Query(None),
    current_user: str = Depends(get_current_user)
):
    try:
        if youtube_url:
            result = await transcribe_youtube_video(youtube_url)
        elif file:
            result = await transcribe_audio_file(file)
        else:
            raise HTTPException(status_code=400, detail="No file or YouTube URL provided.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
