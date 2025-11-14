"""
Pydantic models for photo-related operations.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Request models (what the frontend sends)
class UpdatePhotoRequest(BaseModel):
    """Request to update photo metadata."""
    caption: Optional[str] = None
    approved: Optional[bool] = None  # For moderation

class BulkDeleteRequest(BaseModel):
    """Request to delete multiple photos."""
    photo_ids: List[str] = Field(..., description="List of photo IDs to delete")

class BulkDownloadRequest(BaseModel):
    """Request to download multiple photos."""
    photo_ids: List[str] = Field(..., description="List of photo IDs to download")

# Response models (what the backend returns)
class PhotoResponse(BaseModel):
    """Photo information response."""
    id: str
    event_id: str
    url: str
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    approved: bool = False
    uploaded_at: datetime
    uploaded_by: Optional[str] = None  # User email or anonymous

class PhotoListResponse(BaseModel):
    """Paginated list of photos."""
    photos: List[PhotoResponse]
    total: int
    page: int
    page_size: int
    has_more: bool