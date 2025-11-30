from typing import List, Optional

from sqlalchemy import select, update as sa_update, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from db_example.models.car import Car, EngineType


class CarRepository:
    """
    Repository handling CRUD operations for Car entities.

    Note:
        This repository never commits the session.
        Transaction boundaries are handled by the Unit-of-Work.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_car(
        self,
        make: str,
        model: str,
        year: int,
        color: str,
        price: float,
        engine_type: EngineType,
    ) -> Car:
        car = Car(
            make=make,
            model=model,
            year=year,
            color=color,
            price=price,
            engine_type=engine_type,
        )
        self._session.add(car)
        # Flush to get PK assigned without committing
        await self._session.flush()
        await self._session.refresh(car)
        return car

    async def get_car_by_id(self, car_id: int) -> Optional[Car]:
        stmt = select(Car).where(Car.id == car_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_cars(self) -> List[Car]:
        stmt = select(Car).order_by(Car.id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update_car(self, car_id: int, **fields) -> Optional[Car]:
        # Only allow these fields to be updated
        allowed_fields = {"make", "model", "year", "color", "price", "engine_type"}
        update_data = {k: v for k, v in fields.items() if k in allowed_fields}

        if not update_data:
            # Nothing to update, just return current row
            return await self.get_car_by_id(car_id)

        # Normalize engine_type if passed as string
        if "engine_type" in update_data:
            val = update_data["engine_type"]
            if isinstance(val, str):
                val = EngineType(val.lower())
            update_data["engine_type"] = val

        stmt = (
            sa_update(Car)
            .where(Car.id == car_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(stmt)
        await self._session.flush()

        return await self.get_car_by_id(car_id)

    async def delete_car(self, car_id: int) -> None:
        stmt = sa_delete(Car).where(Car.id == car_id)
        await self._session.execute(stmt)
        await self._session.flush()
