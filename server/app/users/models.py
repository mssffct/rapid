from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base, str_uniq, int_pk, str_null_true
from datetime import date


class User(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    real_name: Mapped[str]
    state: Mapped[str]
    password: Mapped[str] = mapped_column(Text, nullable=False)


    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.name!r},"
                f"real_name={self.real_name!r})")

    def __repr__(self):
        return str(self)