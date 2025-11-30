from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from db_example.db.engine import async_session_factory
from db_example.repositories.car_repository import CarRepository


class CarUnitOfWork:
    """
    Unit-of-Work for car-related operations.

    Usage:

        async with CarUnitOfWork() as uow:
            car = await uow.cars.create_car(...)
    """

    def __init__(self) -> None:
        self.session: Optional[AsyncSession] = None
        self.cars: Optional[CarRepository] = None

    async def __aenter__(self) -> "CarUnitOfWork":
        self.session = async_session_factory()
        self.cars = CarRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        assert self.session is not None

        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()

        await self.session.close()
