from typing import List, Optional
from pydantic import BaseModel, Field

class WordTimestamp(BaseModel):
    start: float
    end: float
    word: str
    probability: Optional[float] = None

class Segment(BaseModel):
    start: float
    end: float
    text: str
    words: Optional[List[WordTimestamp]] = None

class TranscriptionInfo(BaseModel):
    language: str
    language_probability: float
    duration: float
    translation: Optional[str] = None

class TranscriptionResult(BaseModel):
    full_text: str = Field(description="Complete transcription text")
    segments: List[Segment]
    info: TranscriptionInfo

class UserCredentials(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
