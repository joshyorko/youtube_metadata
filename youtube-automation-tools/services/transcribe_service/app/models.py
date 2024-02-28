# models.py
from typing import List, Optional
from pydantic import BaseModel




class WordTimestamp(BaseModel):  # Presuming you might implement word timestamps later
    start: float
    end: float
    word: str
    probability: Optional[float] = None

class Segment(BaseModel):  # Assuming segments could be used for parts of the transcription
    start: float
    end: float
    text: str
    words: Optional[List[WordTimestamp]] = None

class TranscriptionInfo(BaseModel):
    language: str
    language_probability: Optional[float] = None
    duration: Optional[float] = None
    translation: Optional[str] = None

class TranscriptionResult(BaseModel):
    segments: List[Segment]
    info: TranscriptionInfo
