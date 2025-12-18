from typing import List, TYPE_CHECKING
from sqlalchemy import Text, Enum, Table, Column, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID as uuid_type, uuid4

from app.database import Base
from app.core.types import states, auth


if TYPE_CHECKING:
    from app.auth.models import Authenticator


users_groups_association = Table(
    "users_groups",
    Base.metadata,
    Column("user_uuid", UUID, ForeignKey("user_table.uuid"), primary_key=True),
    Column("group_uuid", UUID, ForeignKey("users_group_table.uuid"), primary_key=True),
)


class User(Base):
    __tablename__ = "user_table"
    uuid: Mapped[uuid_type] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    real_name: Mapped[str]
    state: Mapped[str] = mapped_column(
        Enum(states.UserState), nullable=False, default=states.UserState.ACTIVE
    )
    role: Mapped[str] = mapped_column(
        Enum(auth.UserRole), nullable=False, default=auth.UserRole.DEMO
    )
    password: Mapped[str] = mapped_column(Text, nullable=False, default="")
    groups: Mapped[List["UsersGroup"]] = relationship(
        "User", secondary=users_groups_association, back_populates="groups"
    )
    data: Mapped[str] = mapped_column(Text, default="")

    def __str__(self):
        return (
            f"{self.__class__.__name__}(uuid={self.uuid}, "
            f"name={self.name!r},"
            f"role={self.role!r})"
        )

    def __repr__(self):
        return str(self)


class UsersGroup(Base):
    __tablename__ = "users_group_table"
    uuid: Mapped[uuid_type] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]

    users: Mapped[List["User"]] = relationship(
        "UsersGroup", secondary=users_groups_association, back_populates="users"
    )
    auth_uuid: Mapped[uuid_type]
    authenticator: Mapped["Authenticator"] = relationship(
        primaryjoin="UsersGroup.auth_uuid == foreign(Authenticator.uuid)"
    )
