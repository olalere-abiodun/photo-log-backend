"""
Photos router - handles photo moderation endpoints for hosts.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, List

from app.models.photo import (
    PhotoResponse,
    PhotoListResponse,
    UpdatePhotoRequest,
    BulkDeleteRequest,
    BulkDownloadRequest,
)
from app.dependencies import get_current_user
from app.models.auth import MessageResponse

router = APIRouter(prefix="/events", tags=["photos"])

# Helper function to check if user owns the event
# (You'll implement this when you add database)
async def verify_event_ownership(event_id: str, user: Dict[str, Any]) -> bool:
    """
    Verify that the current user owns the event.
    For now, return True (you'll add database check later).
    """
    # TODO: Check database to verify user owns event
    return True

@router.get("/{event_id}/photos", response_model=PhotoListResponse)
async def get_event_photos(
    event_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get paginated list of photos for an event.
    
    Only the event owner (host) can see all photos including unapproved ones.
    """
    # Verify user owns the event
    if not await verify_event_ownership(event_id, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this event's photos"
        )
    
    # TODO: Query database for photos
    # For now, return empty list
    return PhotoListResponse(
        photos=[],
        total=0,
        page=page,
        page_size=page_size,
        has_more=False
    )

@router.patch("/{event_id}/photos/{photo_id}", response_model=PhotoResponse)
async def update_photo(
    event_id: str,
    photo_id: str,
    request: UpdatePhotoRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update photo metadata (caption, approval status).
    """
    # Verify ownership
    if not await verify_event_ownership(event_id, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this event's photos"
        )
    
    # TODO: Update photo in database
    # For now, return a mock response
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Photo update not yet implemented (database needed)"
    )

@router.delete("/{event_id}/photos/{photo_id}", response_model=MessageResponse)
async def delete_photo(
    event_id: str,
    photo_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete a single photo.
    """
    # Verify ownership
    if not await verify_event_ownership(event_id, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this event's photos"
        )
    
    # TODO: Delete photo from database and storage
    return MessageResponse(message=f"Photo {photo_id} deleted successfully")

@router.post("/{event_id}/photos/bulk-delete", response_model=MessageResponse)
async def bulk_delete_photos(
    event_id: str,
    request: BulkDeleteRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete multiple photos at once.
    """
    # Verify ownership
    if not await verify_event_ownership(event_id, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this event's photos"
        )
    
    # TODO: Delete photos from database and storage
    deleted_count = len(request.photo_ids)
    return MessageResponse(
        message=f"Successfully deleted {deleted_count} photo(s)"
    )

@router.post("/{event_id}/photos/bulk-download", response_model=MessageResponse)
async def bulk_download_photos(
    event_id: str,
    request: BulkDownloadRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Trigger download of selected photos (returns download link or ZIP).
    """
    # Verify ownership
    if not await verify_event_ownership(event_id, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to download this event's photos"
        )
    
    # TODO: Create ZIP file and return download link
    return MessageResponse(
        message=f"Download prepared for {len(request.photo_ids)} photo(s)"
    )