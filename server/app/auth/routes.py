from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.auth.schemas import (
    Token,
    User as PydanticUser,
    AuthenticatorBase,
    AuthenticatorCreate,
)
from app.auth.security import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.exceptions import raise_401_exception
from app.auth.dependencies import PermissionManager
from app.auth.models import Authenticator

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_db_session),
) -> Token:
    """
    Obtain jwt token.
    """
    user = await authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        await raise_401_exception("Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/whoami", response_model=PydanticUser)
async def read_users_me(current_user: PydanticUser = Depends(PermissionManager("ALL"))):
    """
    Get user from token
    """
    return current_user


@router.post("/", response_model=AuthenticatorBase)
async def auth_create(
    auth: AuthenticatorCreate,
    current_user: PydanticUser = PermissionManager({"LA", "SA"}),
    db_session: AsyncSession = Depends(get_db_session),
):
    """
    Create authenticator
    :param auth:
    :param current_user:
    :param db_session:
    :return:
    """
    pass


@router.get("/overview", response_model=List[AuthenticatorCreate])
async def auths_overview(
    current_user: PydanticUser = PermissionManager({"LA", "SA"}),
    db_session: AsyncSession = Depends(get_db_session),
):
    """
    List authenticators
    :param current_user:
    :param db_session:
    :return:
    """
    result = await db_session.scalars(select(Authenticator))
    return result.all()
