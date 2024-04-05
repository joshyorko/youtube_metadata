from fastapi import UploadFile
from ..models import (
    TranscriptionResult,
    Segment,
    TranscriptionInfo,
)  # Adjust the import path
import whisper
import asyncio
import aiofiles
import tempfile
import os

# Load the Whisper model globally to optimize resource usage
model = whisper.load_model("small.en")  # Consider adjusting model size as needed


async def transcribe_audio_file(file: UploadFile) -> TranscriptionResult:
    # Create a temporary file using aiofiles for asynchronous file operations
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file_path = temp_file.name
    temp_file.close()  # Close the file to ensure it's not locked

    async with aiofiles.open(temp_file_path, "wb") as temp_aio_file:
        await file.seek(0)  # Reset file pointer to the beginning
        content = await file.read()  # Read file content asynchronously
        await temp_aio_file.write(content)  # Write content to temporary file

    # Perform transcription using Whisper in an asynchronous thread
    try:
        result = await asyncio.to_thread(model.transcribe, temp_file_path)
        print(result["segments"])

        segments = [
            Segment(
                start=0,  # Placeholder start time
                end=result.get("duration", 0),  # Use Whisper's reported duration
                text=result["text"],  # The transcribed text
            )
        ]

        info = TranscriptionInfo(
            language=result.get("language", "unknown"),  # Detected language
            language_probability=result.get(
                "language_probability", 1.0
            ),  # Placeholder probability
            duration=result.get("duration"),  # Audio duration
            translation=result.get("translation"),  # Translated text, if any
        )

        transcription_result = TranscriptionResult(segments=segments, info=info)
    finally:
        os.remove(
            temp_file_path
        )  # Ensure the temporary file is deleted after processing

    return transcription_result
