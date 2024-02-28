# services/transcribe_service/app/routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from .services.transcribe import transcribe_audio_file
from .models import TranscriptionResult


transcribe_router = APIRouter()



@transcribe_router.post("/", response_model=TranscriptionResult)
async def transcribe_route(file: UploadFile = File(...)):
    try:
        result = await transcribe_audio_file(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
