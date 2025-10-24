from fastapi import FastAPI
from core.config import Settings
from api import user, auth
from core.database.session import get_db
from core.connections.database import engine

# Initialize FastAPI app
app = FastAPI(
    title="User Management API",
    version="1.0.0",
    description="API for user management and authentication"
)

# Include routers
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

# Dependency injection for DB session
app.dependency_overrides[get_db] = get_db

# Startup event to ensure DB engine is ready (optional, since engine is created on import)
@app.on_event("startup")
async def startup_event():
    pass  # Engine is already created in core/connections/database.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)