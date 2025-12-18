from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database
from app.services.auth import AuthService
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_database)
):
    """
    Login with JSHSHIR and password.

    Required credentials:
    - jshshir: 14-digit passport number
    - password: 6-digit password

    Returns:
    - access_token: JWT token for authentication
    - token_type: Bearer
    - user: User information (id, full_name, jshshir, roles, phone)
    """
    service = AuthService(db)
    return await service.login(login_data)
