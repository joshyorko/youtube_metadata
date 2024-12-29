import logging
from fastapi import UploadFile
from ..models import (
    TranscriptionResult,
    Segment,
    TranscriptionInfo,
)
import whisper
import asyncio
import aiofiles
import tempfile
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the Whisper model globally to optimize resource usage
model = whisper.load_model("small.en")  # Adjust model size as needed

async def transcribe_audio_file(file: UploadFile) -> TranscriptionResult:
    logger.info("Starting transcription of uploaded audio file.")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file_path = temp_file.name
    temp_file.close()

    async with aiofiles.open(temp_file_path, "wb") as temp_aio_file:
        await file.seek(0)
        content = await file.read()
        await temp_aio_file.write(content)
        logger.info(f"Uploaded file saved to temporary path: {temp_file_path}")

    return await transcribe_file(temp_file_path)

async def transcribe_youtube_video(youtube_url: str) -> TranscriptionResult:
    logger.info(f"Starting transcription of YouTube video: {youtube_url}")
    temp_video = tempfile.NamedTemporaryFile(delete=True, suffix=".mp4")
    temp_video_path = temp_video.name
    temp_video.close()

    try:
        yt = YouTube(youtube_url, on_progress_callback=on_progress)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream is None:
            logger.error("No audio stream available for the provided YouTube URL.")
            raise ValueError("No audio stream available for the provided YouTube URL.")
        audio_stream.download(output_path=os.path.dirname(temp_video_path), filename=os.path.basename(temp_video_path))
        logger.info(f"YouTube video downloaded to temporary path: {temp_video_path}")
    except Exception as e:
        logger.error(f"Error downloading YouTube video: {e}")
        raise

    return await transcribe_file(temp_video_path)

async def transcribe_file(file_path: str) -> TranscriptionResult:
    logger.info(f"Starting transcription of file: {file_path}")
    try:
        result = await asyncio.to_thread(model.transcribe, file_path)
        logger.info("Transcription completed successfully.")

        segments = [
            Segment(
                start=0,
                end=result.get("duration", 0),
                text=result["text"],
            )
        ]

        info = TranscriptionInfo(
            language=result.get("language", "unknown"),
            language_probability=result.get("language_probability", 1.0),
            duration=result.get("duration"),
            translation=result.get("translation"),
        )

        transcription_result = TranscriptionResult(segments=segments, info=info)
    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        raise
    finally:
        os.remove(file_path)
        logger.info(f"Temporary file removed: {file_path}")

    return transcription_result
