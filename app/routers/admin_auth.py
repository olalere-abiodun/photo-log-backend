"""
Admin authentication router - handles all /admin/auth/* endpoints.
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.models.auth import TokenRequest, SigninResponse, UserResponse, MessageResponse
from app.dependencies import get_current_admin_user
from app.services.firebase import verify_firebase_token

router = APIRouter(prefix="/admin/auth", tags=["admin-auth"])


@router.post("/signin", response_model=SigninResponse)
async def admin_signin(request: TokenRequest):
    """
    Admin login - verify Firebase token and check admin role.
    
    For now: Checks if email is in admin_emails list.
    Later: Check is_admin flag in database.
    """
    # Verify the Firebase token
    user_info = verify_firebase_token(request.token)
    
    # Check if user is admin
    from app.config import settings
    
    user_email = user_info.get("email")
    if not user_email or user_email not in settings.get_admin_emails_list():
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
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


@router.post("/signout", response_model=MessageResponse)
async def admin_signout():
    """
    Admin sign out - invalidate session/token.
    
    Frontend handles Firebase signout (revokes token client-side).
    Backend just returns success.
    """
    return MessageResponse(message="Signed out successfully")


@router.post("/refresh", response_model=SigninResponse)
async def admin_refresh(
    request: TokenRequest,
    admin: Dict[str, Any] = Depends(get_current_admin_user)
):
    """
    Refresh admin authentication token.
    
    Verifies token and checks admin role.
    """
    # Verify the new Firebase token
    user_info = verify_firebase_token(request.token)
    
    # Check admin role again
    from app.config import settings
    
    user_email = user_info.get("email")
    if not user_email or user_email not in settings.get_admin_emails_list():
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
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

