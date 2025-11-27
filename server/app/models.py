from sqlalchemy import Text, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, int_pk
from app.core_types import states, auth


class User(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    real_name: Mapped[str]
    state: Mapped[str] = mapped_column(
        Enum(states.UserStates), nullable=False, default=states.UserStates.ACTIVE
    )
    role: Mapped[str] = mapped_column(
        Enum(auth.UserRoles), nullable=False, default=auth.UserRoles.DEMO
    )
    password: Mapped[str] = mapped_column(Text, nullable=False, default="")

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"name={self.name!r},"
            f"role={self.role!r})"
        )

    def __repr__(self):
        return str(self)
