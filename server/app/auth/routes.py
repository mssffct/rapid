from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.type_responses import TypeWithImageResponse
from app.core.types import auth as auth_types, states
from app.core.utils import modfinder
from app.database import get_db_session
from app.auth.schemas import (
    Token,
    User as PydanticUser,
    AuthenticatorCreate,
    AuthenticatorResponse,
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


@router.post("/", response_model=AuthenticatorResponse)
async def auth_create(
    auth: AuthenticatorCreate,
    current_user: PydanticUser = Depends(PermissionManager({"LA", "SA"})),
    db_session: AsyncSession = Depends(get_db_session),
):
    """
    Create authenticator
    """
    try:
        new_auth = AuthenticatorCreate(
            name=auth.name,
            auth_type=auth.auth_type,
            state=auth.state or states.AvailabilityState.ACTIVE,
            priority=auth.priority,
            mfa=auth.mfa,
        )
        db_session.add(new_auth)
        await db_session.commit()
        await db_session.refresh(new_auth)
        return AuthenticatorResponse(
            uuid=new_auth.uuid, name=new_auth.name, auth_type=new_auth.auth_type
        )
    except Exception as e:
        print(e)


@router.get("/overview", response_model=List[AuthenticatorCreate])
async def auths_overview(
    current_user: PydanticUser = Depends(PermissionManager({"LA", "SA"})),
    db_session: AsyncSession = Depends(get_db_session),
):
    """
    List authenticators
    """
    result = await db_session.scalars(select(Authenticator))
    return result.all()


@router.get("/types/{ins_type}", response_model=List[TypeWithImageResponse])
async def types(
    ins_type: str,
    current_user: PydanticUser = Depends(PermissionManager({"LA", "SA"})),
):
    """
    List authenticators types
    """
    result = []
    match ins_type:
        case auth_types.AuthInstances.AUTH:
            result = await modfinder.load_modules("auth/auths", "authenticator")
        case auth_types.AuthInstances.MFA:
            result = await modfinder.load_modules("auth/mfas", "mfa")
        case _:
            pass
    return [item.get_type_info(item) for item in result]
