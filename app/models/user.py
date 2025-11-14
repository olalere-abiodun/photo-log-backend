"""
Pydantic models for user-related operations.
Currently simplified since we're not using a database yet.
"""
from pydantic import BaseModel
from typing import Optional


class UserProfile(BaseModel):
    """User profile model (from Firebase token for now)."""
    uid: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    
    # These will be added when database is implemented:
    # plan: Optional[str] = None
    # limits: Optional[Dict[str, int]] = None

