"""
Authentication router - handles all /auth/* endpoints.
"""
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

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=SigninResponse)
async def signup(request: TokenRequest):
    """
    Register a new host user.
    
    Supports both email/password and Google sign-in via Firebase.
    Frontend handles Firebase signup directly (email/password or Google OAuth),
    then sends the ID token here. Backend verifies the token and returns user info.
    """
    # Verify the Firebase token
    user_info = verify_firebase_token(request.token)
    
    # Extract user information from token
    user_response = UserResponse(
        uid=user_info["uid"],
        email=user_info.get("email"),
        email_verified=user_info.get("email_verified", False),
        name=user_info.get("name"),
    )
    
    # Later: Create user profile in database here
    # For now, just return info from token
    
    return SigninResponse(
        token=request.token,
        user=user_response
    )


@router.post("/signin", response_model=SigninResponse)
async def signin(request: TokenRequest):
    """
    Host login - verify Firebase token and return user info.
    
    Supports both email/password and Google sign-in via Firebase.
    Frontend handles Firebase signin directly (email/password or Google OAuth),
    then sends the ID token here. Backend verifies the token and returns user info.
    """
    # Verify the Firebase token
    user_info = verify_firebase_token(request.token)
    
    # Extract user information from token
    user_response = UserResponse(
        uid=user_info["uid"],
        email=user_info.get("email"),
        email_verified=user_info.get("email_verified", False),
        name=user_info.get("name"),
    )
    
    # Later: Check if user exists in database, create if needed
    # For now, just return info from token
    
    return SigninResponse(
        token=request.token,
        user=user_response
    )


@router.post("/signout", response_model=MessageResponse)
async def signout():
    """
    Sign out - invalidate session/token.
    
    Frontend handles Firebase signout (revokes token client-side).
    Backend just returns success.
    """
    return MessageResponse(message="Signed out successfully")


@router.post("/refresh", response_model=SigninResponse)
async def refresh(request: TokenRequest):
    """
    Refresh authentication token.
    
    Frontend gets new token from Firebase, backend verifies it.
    """
    # Verify the new Firebase token
    user_info = verify_firebase_token(request.token)
    
    # Extract user information from token
    user_response = UserResponse(
        uid=user_info["uid"],
        email=user_info.get("email"),
        email_verified=user_info.get("email_verified", False),
        name=user_info.get("name"),
    )
    
    return SigninResponse(
        token=request.token,
        user=user_response
    )


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(request: VerifyEmailRequest):
    """
    Confirm email verification.
    
    Frontend handles email verification with Firebase.
    Backend receives verified token and confirms verification.
    """
    # Verify the token (which already has updated email_verified status)
    user_info = verify_firebase_token(request.token)
    
    # Later: Update user's email_verified status in database
    # For now, token already contains the updated status
    
    return MessageResponse(message="Email verified successfully")


@router.post("/resend-verification", response_model=MessageResponse)
async def resend_verification():
    """
    Resend email verification link.
    
    Frontend calls Firebase to resend verification email.
    Backend just returns success.
    """
    return MessageResponse(message="Verification email sent")


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(request: ForgotPasswordRequest):
    """
    Send password reset email.
    
    Frontend calls Firebase to send password reset email.
    Backend just returns success.
    """
    # Frontend handles the actual password reset email sending via Firebase
    return MessageResponse(message="Password reset email sent")


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(request: ResetPasswordRequest):
    """
    Confirm password reset and set new password.
    
    Frontend handles password reset with Firebase.
    Backend receives new token after reset and verifies it.
    """
    # Verify the new token after password reset
    verify_firebase_token(request.token)
    
    return MessageResponse(message="Password reset successfully")


