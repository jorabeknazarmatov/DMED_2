from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.utils.generators import generate_password
from app.core.exceptions import not_found_exception, already_exists_exception
from app.core.logging import get_logger

logger = get_logger(__name__)


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def get_all_users(self) -> list[UserListResponse]:
        """Get all users (admin only)."""
        logger.info("Fetching all users")
        users = await self.user_repo.get_all()
        return [UserListResponse.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """Get user by ID."""
        logger.info(f"Fetching user with id={user_id}")
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise not_found_exception("User", user_id)
        return UserResponse.model_validate(user)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create new user with auto-generated password, or add roles to existing user."""
        logger.info(f"Creating user: {user_data.full_name} (jshshir={user_data.jshshir})")

        # Check if JSHSHIR already exists
        existing_user = await self.user_repo.get_by_jshshir(user_data.jshshir)
        if existing_user:
            logger.info(f"User with jshshir={user_data.jshshir} already exists. Adding new roles.")

            # Merge roles (avoid duplicates)
            existing_roles = set(existing_user.roles)
            new_roles = set(user_data.roles)
            merged_roles = list(existing_roles | new_roles)

            # Update user with merged roles
            update_data = UserUpdate(roles=merged_roles)
            updated_user = await self.user_repo.update(existing_user, update_data)

            logger.info(
                f"Roles added to existing user: {updated_user.full_name} "
                f"(id={updated_user.id}, old_roles={list(existing_roles)}, new_roles={merged_roles})"
            )

            return UserResponse.model_validate(updated_user)

        # Generate 6-digit password
        password = generate_password()

        # Create user
        user = await self.user_repo.create(user_data, password)

        logger.info(
            f"User created successfully: {user.full_name} "
            f"(id={user.id}, jshshir={user.jshshir}, password={password})"
        )

        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """Update user."""
        logger.info(f"Updating user with id={user_id}")

        # Get existing user
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise not_found_exception("User", user_id)

        # Check if new JSHSHIR already exists (if changing)
        if user_data.jshshir and user_data.jshshir != user.jshshir:
            existing_user = await self.user_repo.get_by_jshshir(user_data.jshshir)
            if existing_user:
                raise already_exists_exception("User", "jshshir", user_data.jshshir)

        # Update user
        updated_user = await self.user_repo.update(user, user_data)

        logger.info(f"User updated successfully: id={user_id}")

        return UserResponse.model_validate(updated_user)

    async def delete_user(self, user_id: int) -> None:
        """Delete user."""
        logger.info(f"Deleting user with id={user_id}")

        # Get existing user
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise not_found_exception("User", user_id)

        # Delete user
        await self.user_repo.delete(user)

        logger.info(f"User deleted successfully: id={user_id}")
