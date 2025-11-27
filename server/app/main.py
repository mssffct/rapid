from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import init_db, get_db_session
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router # Подключаем роутер для пользователей
from app.auth.schemas import User as PydanticUser
from app.auth.dependencies import get_current_user, get_current_active_user

# --- Запуск и остановка приложения ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="FastAPI Token Auth with PostgreSQL & Docker Compose",
    description="A complete example of token-based authentication with FastAPI, PostgreSQL, and structured code.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(users_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Token Auth Example!"}

@app.get("/items/", tags=["items"])
async def read_items(current_user: PydanticUser = Depends(get_current_user)):
    """
    Пример защищенного эндпоинта.
    Доступен только для аутентифицированных пользователей.
    """
    return [
        {"item_id": "Foo", "owner": current_user.name},
        {"item_id": "Bar", "owner": current_user.name}
    ]

@app.get("/admin_data/", tags=["admin"])
async def read_admin_data(current_user: PydanticUser = Depends(get_current_active_user)):
    """
    Пример эндпоинта, который может быть доступен только администраторам.
    """
    if current_user.name != "john.doe":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only specific users can access this resource"
        )
    return {"message": f"Welcome, admin {current_user.name}! Here is sensitive data."}