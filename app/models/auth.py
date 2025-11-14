"""
Pydantic models for authentication requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class TokenRequest(BaseModel):
    """Request model for endpoints that receive Firebase ID token."""
    token: str = Field(..., description="Firebase ID token")


class UserResponse(BaseModel):
    """User information response model."""
    uid: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None


class SigninResponse(BaseModel):
    """Response model for signin/signup endpoints."""
    token: str
    user: UserResponse


class VerifyEmailRequest(BaseModel):
    """Request model for email verification."""
    token: str = Field(..., description="Firebase ID token after email verification")


class ForgotPasswordRequest(BaseModel):
    """Request model for forgot password (frontend handles, backend just acknowledges)."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Request model for password reset."""
    token: str = Field(..., description="Firebase ID token after password reset")


class UpdateProfileRequest(BaseModel):
    """Request model for updating user profile."""
    name: Optional[str] = None


class MessageResponse(BaseModel):
    """Generic success message response."""
    message: str

