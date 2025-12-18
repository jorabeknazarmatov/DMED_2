from fastapi import APIRouter
from app.api.v1 import patients, locations, admin, users, auth

# Create v1 API router
api_router = APIRouter(prefix="/api/v1")

# Include all routers
api_router.include_router(auth.router)
api_router.include_router(patients.router)
api_router.include_router(locations.router)
api_router.include_router(admin.router)
api_router.include_router(users.router)
