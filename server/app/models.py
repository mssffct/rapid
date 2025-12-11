from sqlalchemy import Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

from app.database import Base
from app.core.types import states, auth


class User(Base):
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    real_name: Mapped[str]
    state: Mapped[str] = mapped_column(
        Enum(states.UserState), nullable=False, default=states.UserState.ACTIVE
    )
    role: Mapped[str] = mapped_column(
        Enum(auth.UserRole), nullable=False, default=auth.UserRole.DEMO
    )
    password: Mapped[str] = mapped_column(Text, nullable=False, default="")
    data: Mapped[str] = mapped_column(Text, default="")

    def __str__(self):
        return (
            f"{self.__class__.__name__}(uuid={self.uuid}, "
            f"name={self.name!r},"
            f"role={self.role!r})"
        )

    def __repr__(self):
        return str(self)

    def is_admin(self):
        """Check if user has admin rights"""
        return self.role in (auth.UserRole.STAFF_ADMIN, auth.UserRole.LICENSE_ADMIN)
