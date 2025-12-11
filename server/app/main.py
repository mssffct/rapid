from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status

from app.database import init_db
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.auth.schemas import User as PydanticUser
from app.auth.dependencies import get_current_user
from app.core.types.states import UserState


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Broker Rapid",
    description="VDI management tool",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/api/v1")
async def root():
    return {"message": "Welcome to the FastAPI Token Auth Example!"}


@app.get("/api/v1/admin_routes/", tags=["admin_routes"])
async def read_admin_data(current_user: PydanticUser = Depends(get_current_user)):
    """
    Get admin routes
    """
    if current_user.state == UserState.ACTIVE and current_user.is_admin():
        return {"result": ["here admins routes"]}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only specific users can access this resource",
        )
