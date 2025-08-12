from pydantic import BaseModel
from typing import List, Optional

class ChunkedDocument(BaseModel):
    filename: str
    total_chunks: int
    chunks: List[str]

class UploadResponse(BaseModel):
    message: str
    download_url: str
    file_size: Optional[int] = None
    processing_time: Optional[float] = None

class UploadRequest(BaseModel):
    file_type: str
    process_type: Optional[str] = "complete"  # complete, analysis_only, risk_only