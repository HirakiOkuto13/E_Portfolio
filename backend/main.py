import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test endpoint without router imports
@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}"
    }

# Import routers after app creation to avoid circular imports
try:
    from app.api.v1.endpoints import auth, profiles, activities, awards
    
    # Include routers
    app.include_router(
        auth.router,
        prefix=settings.API_V1_STR,
        tags=["authentication"]
    )
    app.include_router(
        profiles.router,
        prefix=f"{settings.API_V1_STR}/profiles",
        tags=["profiles"]
    )
    app.include_router(
        activities.router,
        prefix=f"{settings.API_V1_STR}/activities",
        tags=["activities"]
    )
    app.include_router(
        awards.router,
        prefix=f"{settings.API_V1_STR}/awards",
        tags=["awards"]
    )
    logger.info("All routers loaded successfully")
except Exception as e:
    logger.error(f"Error loading routers: {str(e)}")
    raise