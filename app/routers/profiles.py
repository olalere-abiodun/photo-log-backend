from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from app.models.auth import (
    TokenRequest,
    SigninResponse,
    UserResponse,
    VerifyEmailRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UpdateProfileRequest,
    MessageResponse,
)
from app.dependencies import get_current_user
from app.services.firebase import verify_firebase_token

router = APIRouter(prefix="/me", tags=["me"])

# Protected routes (require authentication)

@router.get("", response_model=UserResponse)
async def get_current_user_profile(
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get current host profile.
    
    Returns user information from verified token.
    Later: Query database for user profile with plan/limits.
    """
    return UserResponse(
        uid=user["uid"],
        email=user.get("email"),
        email_verified=user.get("email_verified", False),
        name=user.get("name"),
    )


@router.patch("", response_model=UserResponse)
async def update_profile(
    request: UpdateProfileRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update profile settings (name, contact).
    
    For now: Just return success with updated info.
    Later: Update user profile in database.
    """
    # For now, just acknowledge the update
    # Later: Update user profile in database
    
    return UserResponse(
        uid=user["uid"],
        email=user.get("email"),
        email_verified=user.get("email_verified", False),
        name=request.name if request.name else user.get("name"),
    )


@router.patch("/password", response_model=MessageResponse)
async def change_password(
    request: TokenRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Change password (authenticated).
    
    Frontend handles password change with Firebase.
    Backend receives new token after password change and verifies it.
    """
    # Verify the new token after password change
    verify_firebase_token(request.token)
    
    return MessageResponse(message="Password changed successfully")

