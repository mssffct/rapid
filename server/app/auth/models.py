from typing import List, TYPE_CHECKING
from uuid import UUID
from sqlalchemy import Enum, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlmodel import UniqueConstraint

from app.database import ManagedDBModel
from app.core.types import states, auth


if TYPE_CHECKING:
    from app.users.models import UsersGroup


class Authenticator(ManagedDBModel):
    __tablename__ = "authenticator_table"
    _table_args__ = (
        UniqueConstraint("name", "auth_type", name="unique_auth_name_constraint"),
    )

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
    mfa: Mapped[UUID] = mapped_column(ForeignKey("mfa_table.uuid"), nullable=True)
    users_groups: Mapped[List["UsersGroup"]] = relationship(
        back_populates="authenticator",
        primaryjoin="Authenticator.uuid == foreign(UsersGroup.auth_uuid)",
    )


class MFA(ManagedDBModel):
    __tablename__ = "mfa_table"

    name: Mapped[str]
    mfa_type: Mapped[str] = mapped_column(
        Enum(auth.MFAType), nullable=False, default=auth.MFAType.TOTP
    )
    state: Mapped[str] = mapped_column(
        Enum(states.AvailabilityState),
        nullable=False,
        default=states.AvailabilityState.ACTIVE,
    )
