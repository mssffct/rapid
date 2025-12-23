from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status

from app.database import init_db
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.auth.schemas import User as PydanticUser
from app.auth.dependencies import PermissionManager
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


@app.get("/api/v1/routes_available", tags=["routes"])
async def read_routes(current_user: PydanticUser = Depends(PermissionManager("ALL"))):
    """
    Get admin routes
    """
    if current_user.state == UserState.ACTIVE:
        match current_user.is_admin():
            case True:
                return {"result": ["here admins routes"]}
            case _:
                return {"result": ["here plain users roles"]}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only specific users can access this resource",
        )
