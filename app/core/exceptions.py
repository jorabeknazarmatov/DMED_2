from fastapi import HTTPException, status


class BaseAppException(Exception):
    """Base exception for application."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundException(BaseAppException):
    """Exception for not found resources."""
    pass


class AlreadyExistsException(BaseAppException):
    """Exception for duplicate resources."""
    pass


class ValidationException(BaseAppException):
    """Exception for validation errors."""
    pass


class DatabaseException(BaseAppException):
    """Exception for database errors."""
    pass


def not_found_exception(resource: str, resource_id: int | str):
    """Return HTTPException for not found resource."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} with id={resource_id} not found"
    )


def already_exists_exception(resource: str, field: str, value: str):
    """Return HTTPException for duplicate resource."""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{resource} with {field}={value} already exists"
    )


def validation_exception(message: str):
    """Return HTTPException for validation error."""
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=message
    )


def internal_server_exception(message: str = "Internal server error"):
    """Return HTTPException for internal server error."""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=message
    )
