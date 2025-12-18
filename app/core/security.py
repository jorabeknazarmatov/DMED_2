"""
Security module for authentication/authorization.
Basic HTTP authentication for admin endpoints.
Prepared for JWT implementation in the future.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core.config import settings

# HTTP Basic Auth (simple version for admin)
security = HTTPBasic()


def verify_admin_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> bool:
    """
    Verify admin credentials using HTTP Basic Auth.
    Returns True if credentials are valid, raises HTTPException otherwise.
    """
    is_username_correct = credentials.username == settings.ADMIN_USERNAME
    is_password_correct = credentials.password == settings.ADMIN_PASSWORD

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return True


# TODO: Add JWT token generation and validation
# TODO: Add password hashing utilities (bcrypt)
# TODO: Add role-based access control (RBAC)
