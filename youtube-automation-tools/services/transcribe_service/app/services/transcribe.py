import logging
from fastapi import UploadFile
from ..models import (
    TranscriptionResult,
    Segment,
    TranscriptionInfo,
)
from faster_whisper import WhisperModel
import asyncio
import aiofiles
import tempfile
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the model with better performance settings
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
    local_files_only=False,  # Allow downloading if model not found locally
    download_root=None,  # Use default download location
    cpu_threads=4,  # Adjust based on your CPU cores
    num_workers=2,  # Number of workers for parallel processing
    beam_size=5,  # Default beam size for better accuracy
    condition_on_previous_text=True,  # Help maintain context between segments
    no_speech_threshold=0.6,  # Whisper default, works well with VAD
    compression_ratio_threshold=2.4,  # Whisper default
    log_prob_threshold=-1.0  # Whisper default
)

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
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video_path = temp_video.name
    temp_video.close()

    try:
        logger.info("Initializing YouTube download...")
        yt = YouTube(youtube_url, on_progress_callback=on_progress)
        logger.info(f"Video info - Title: '{yt.title}', Duration: {yt.length}s")
        
        # Get all available audio streams
        audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
        logger.info(f"Available audio streams: {[f'{s.itag}: {s.abr}' for s in audio_streams]}")
        
        # Select highest quality audio stream
        audio_stream = audio_streams.first()
        if audio_stream is None:
            logger.error("No audio stream available for the provided YouTube URL.")
            raise ValueError("No audio stream available for the provided YouTube URL.")
            
        logger.info(f"Selected audio stream: itag={audio_stream.itag}, abr={audio_stream.abr}, "
                   f"mime_type={audio_stream.mime_type}, codec={audio_stream.audio_codec}")
        
        logger.info(f"Downloading audio to: {temp_video_path}")
        audio_stream.download(output_path=os.path.dirname(temp_video_path), 
                            filename=os.path.basename(temp_video_path))
                            
        if not os.path.exists(temp_video_path):
            raise ValueError("Failed to download audio file")
            
        file_size = os.path.getsize(temp_video_path)
        logger.info(f"Downloaded audio file size: {file_size} bytes")
        
        if file_size == 0:
            raise ValueError("Downloaded audio file is empty")

        # Verify audio file is valid
        try:
            import av
            with av.open(temp_video_path) as container:
                audio_stream = next(s for s in container.streams if s.type == 'audio')
                logger.info(f"Audio file validation - Format: {container.format.name}, "
                          f"Duration: {float(container.duration) / av.time_base}, "
                          f"Sample rate: {audio_stream.sample_rate}Hz, "
                          f"Channels: {audio_stream.channels}")
        except Exception as e:
            logger.error(f"Error validating audio file: {e}")
            raise ValueError(f"Invalid audio file downloaded: {e}")
            
        return await transcribe_file(temp_video_path)
        
    except Exception as e:
        logger.error(f"Error downloading/processing YouTube video: {str(e)}")
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        raise

def debug_vad_output(segments_list, info, vad_params):
    """Helper function to debug VAD output"""
    logger.debug("VAD Debug Information:")
    logger.debug(f"VAD Parameters used: {vad_params}")
    logger.debug(f"Total duration: {info.duration}s")
    logger.debug(f"Duration after VAD: {info.duration_after_vad}s")
    logger.debug(f"Audio filtered: {info.duration - info.duration_after_vad:.2f}s")
    logger.debug(f"Number of segments: {len(segments_list)}")
    
    if segments_list:
        logger.debug("First 3 segments:")
        for i, seg in enumerate(segments_list[:3]):
            logger.debug(f"Segment {i}: {seg.start:.2f}s -> {seg.end:.2f}s: {seg.text[:50]}...")
            if hasattr(seg, 'words') and seg.words:
                logger.debug(f"Words in segment {i}: {len(seg.words)}")
    else:
        logger.debug("No segments detected!")

async def transcribe_file(file_path: str) -> TranscriptionResult:
    logger.info(f"Starting transcription of file: {file_path}")
    
    try:
        if not os.path.exists(file_path):
            raise ValueError(f"File does not exist: {file_path}")
        
        file_size = os.path.getsize(file_path)
        logger.info(f"File size: {file_size} bytes")
        
        # Initial VAD settings based on Silero VAD defaults
        vad_params = {
            "threshold": 0.5,
            "min_speech_duration_ms": 250,
            "max_speech_duration_s": float("inf"),
            "min_silence_duration_ms": 2000,
            "speech_pad_ms": 400,
            "neg_threshold": 0.35
        }
        
        logger.info("Starting transcription with initial VAD settings...")
        segments, info = await asyncio.to_thread(
            model.transcribe, 
            file_path,
            beam_size=5,
            word_timestamps=True,  # Enable word timestamps
            vad_filter=True,
            vad_parameters=vad_params
        )
        
        segments_list = list(segments)
        debug_vad_output(segments_list, info, vad_params)
        
        if len(segments_list) == 0:
            logger.warning("No segments detected with initial VAD settings")
            
            # Try more lenient VAD settings
            vad_params.update({
                "threshold": 0.3,
                "min_speech_duration_ms": 100,
                "min_silence_duration_ms": 1000,
                "speech_pad_ms": 500,
                "neg_threshold": 0.2
            })
            
            logger.info("Retrying with more lenient VAD settings...")
            segments, info = await asyncio.to_thread(
                model.transcribe, 
                file_path,
                beam_size=5,
                word_timestamps=True,
                vad_filter=True,
                vad_parameters=vad_params
            )
            
            segments_list = list(segments)
            debug_vad_output(segments_list, info, vad_params)
        
        # Process segments with word timestamps
        processed_segments = []
        full_text_parts = []
        
        for segment in segments_list:
            words = []
            if hasattr(segment, 'words') and segment.words:
                words = [
                    WordTimestamp(
                        start=word.start,
                        end=word.end,
                        word=word.word,
                        probability=getattr(word, 'probability', None)
                    )
                    for word in segment.words
                ]
            
            processed_segments.append(
                Segment(
                    start=segment.start,
                    end=segment.end,
                    text=segment.text.strip(),
                    words=words
                )
            )
            full_text_parts.append(segment.text.strip())

        full_text = " ".join(full_text_parts)
        total_duration = max(segment.end for segment in processed_segments) if processed_segments else info.duration

        transcription_result = TranscriptionResult(
            full_text=full_text,
            segments=processed_segments,
            info=TranscriptionInfo(
                language=info.language,
                language_probability=info.language_probability,
                duration=total_duration,
                translation=None
            )
        )
        
        logger.info(f"Transcription complete: {len(processed_segments)} segments")
        logger.info(f"Total duration: {total_duration:.2f}s")
        logger.info(f"Language: {info.language} (probability: {info.language_probability:.2f})")
        
        return transcription_result
        
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        logger.exception("Full traceback:")
        raise
    finally:
        try:
            os.remove(file_path)
            logger.info(f"Temporary file removed: {file_path}")
        except Exception as e:
            logger.error(f"Error removing temporary file: {e}")

    return transcription_result
