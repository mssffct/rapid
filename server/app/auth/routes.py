from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.type_responses import TypeWithImageResponse
from app.core.types import auth as auth_types, states
from app.core.utils import modfinder
from app.database import get_db_session
from app.auth.schemas import (
    LoginResponse,
    User as PydanticUser,
    AuthenticatorCreate,
    AuthenticatorResponse,
    LoginForm,
)
from app.auth.security import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.exceptions import raise_401_exception
from app.auth.dependencies import PermissionManager
from app.auth.models import Authenticator
from app.auth.crud import get_authenticator
from app.core.consts import RPD_COOKIE_NAME

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    form_data: LoginForm = Depends(),
    db_session: AsyncSession = Depends(get_db_session),
) -> LoginResponse:
    """
    Authenticate user with authenticator and mfa (if required) to get token
    1) Check if authenticator exists and not disabled
    2) Check if broker cookie in request
    3) Ask cache manager for number of failed login attempts. If it exceeds
    the number specified in app config - unauthenticated response and block for time specified in
    app config.
    3) Check credentials (or register user) by authenticator
    4) If mfa is enabled ask cache manager for current mfa state if it passed, failed or skipped (results are stored for
    time specified in app config)
    If mfa not passed unauthenticated response with mfa_required result returned
    If mfa is skipped or passed provide token
    """
    if not form_data.authenticator:
        await raise_401_exception("No authenticator uuid provided")
    try:
        auth = await get_authenticator(db_session, form_data.authenticator)
    except ValueError as e:
        await raise_401_exception(str(e))
    if RPD_COOKIE_NAME not in request.cookies:
        await raise_401_exception("Access from unknown source")
    # TODO cache manager request for login attempts

    user = await authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        await raise_401_exception("Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return LoginResponse(
        access_token=access_token, token_type="bearer", result="success"
    )


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
