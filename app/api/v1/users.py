from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.core.security import verify_admin_credentials

router = APIRouter(prefix="/admin/users", tags=["Admin - Users"])


@router.get("/", response_model=list[UserListResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_database),
    _: bool = Depends(verify_admin_credentials)
):
    """
    Get all users (admin only).
    Returns full_name, roles, jshshir, password, phone for all users.

    Requires admin authentication.
    """
    service = UserService(db)
    return await service.get_all_users()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_database),
    _: bool = Depends(verify_admin_credentials)
):
    """
    Create new user (admin only).
    Automatically generates 6-digit password.

    Required fields:
    - full_name: User's full name
    - jshshir: 14-digit passport number (unique)
    - roles: List of roles (manager, shifokor, amaliyot_hamshirasi, royhatga_oluvchi, patronaj_hamshirasi)
    - gender: male or female
    - birth_date: Date of birth
    - phone: Optional phone number

    Requires admin authentication.
    """
    service = UserService(db)
    return await service.create_user(user_data)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_database),
    _: bool = Depends(verify_admin_credentials)
):
    """
    Get user by ID (admin only).

    Requires admin authentication.
    """
    service = UserService(db)
    return await service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_database),
    _: bool = Depends(verify_admin_credentials)
):
    """
    Update user by ID (admin only).

    Requires admin authentication.
    """
    service = UserService(db)
    return await service.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_database),
    _: bool = Depends(verify_admin_credentials)
):
    """
    Delete user by ID (admin only).

    Requires admin authentication.
    """
    service = UserService(db)
    await service.delete_user(user_id)
