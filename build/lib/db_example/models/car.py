from enum import Enum

from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from db_example.db.base import Base


class EngineType(str, Enum):
    PETROL = "petrol"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    make: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[str] = mapped_column(String(30), nullable=False)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)

    # Mandatory field, no DB default
    engine_type: Mapped[EngineType] = mapped_column(
        String(20),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"Car(id={self.id!r}, make={self.make!r}, model={self.model!r}, "
            f"year={self.year!r}, color={self.color!r}, price={self.price!r}, "
            f"engine_type={self.engine_type!r})"
        )
