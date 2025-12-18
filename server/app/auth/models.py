from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlalchemy import Enum, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.core.types import states, auth


if TYPE_CHECKING:
    from app.users.models import UsersGroup


class Authenticator(Base):
    __tablename__ = "authenticator_table"
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    auth_type: Mapped[str] = mapped_column(
        Enum(auth.AuthType), nullable=False, default=auth.AuthType.DB
    )
    state: Mapped[str] = mapped_column(
        Enum(states.AvailabilityState),
        nullable=False,
        default=states.AvailabilityState.ACTIVE,
    )
    priority: Mapped[int] = mapped_column(Integer, default=0)
    mfa: Mapped[UUID] = mapped_column(ForeignKey("mfa_table.uuid"))
    users_groups: Mapped[List["UsersGroup"]] = relationship(
        back_populates="authenticator",
        primaryjoin="Authenticator.uuid == foreign(UsersGroup.auth_uuid)",
    )


class MFA(Base):
    __tablename__ = "mfa_table"
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    mfa_type: Mapped[str] = mapped_column(
        Enum(auth.MFAType), nullable=False, default=auth.MFAType.TOTP
    )
    state: Mapped[str] = mapped_column(
        Enum(states.AvailabilityState),
        nullable=False,
        default=states.AvailabilityState.ACTIVE,
    )
