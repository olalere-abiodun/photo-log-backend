"""
Firebase Admin SDK initialization and token verification.
"""
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, status
from pathlib import Path
from typing import Dict, Any
import logging

from app.config import get_firebase_credentials_path

logger = logging.getLogger(__name__)

# Global variable to track if Firebase is initialized
_firebase_initialized = False


def initialize_firebase() -> None:
    """
    Initialize Firebase Admin SDK using service account credentials.
    This should be called once at application startup.
    """
    global _firebase_initialized
    
    if _firebase_initialized:
        logger.info("Firebase Admin SDK already initialized")
        return
    
    try:
        cred_path = get_firebase_credentials_path()
        
        if not cred_path.exists():
            raise FileNotFoundError(
                f"Firebase credentials file not found at {cred_path}. "
                "Please download your service account JSON from Firebase Console."
            )
        
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(str(cred_path))
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        logger.info("Firebase Admin SDK initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
        raise


def verify_firebase_token(token: str) -> Dict[str, Any]:
    """
    Verify a Firebase ID token and return decoded token information.
    
    Args:
        token: Firebase ID token string
        
    Returns:
        Dictionary containing user information from decoded token:
        - uid: Firebase user ID
        - email: User email
        - email_verified: Whether email is verified
        - Additional claims from token
        
    Raises:
        HTTPException: If token is invalid, expired, or revoked
    """
    if not _firebase_initialized:
        initialize_firebase()
    
    try:
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        
        # Extract user information
        user_info = {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "email_verified": decoded_token.get("email_verified", False),
            "name": decoded_token.get("name"),
            "firebase_claims": decoded_token  # Include all claims for reference
        }
        
        return user_info
        
    except auth.InvalidIdTokenError:
        logger.warning("Invalid Firebase ID token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    except auth.ExpiredIdTokenError:
        logger.warning("Expired Firebase ID token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired"
        )
    except auth.RevokedIdTokenError:
        logger.warning("Revoked Firebase ID token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has been revoked"
        )
    except Exception as e:
        logger.error(f"Error verifying Firebase token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error verifying authentication token"
        )

