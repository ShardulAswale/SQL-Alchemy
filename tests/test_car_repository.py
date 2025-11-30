import pytest

from db_example.models.car import EngineType
from db_example.repositories.car_repository import CarRepository


pytestmark = pytest.mark.asyncio


async def test_insert_and_fetch(db_session):
    repo = CarRepository(db_session)

    created = await repo.create_car(
        make="TestMake",
        model="TestModel",
        year=2020,
        color="Red",
        price=12345.67,
        engine_type=EngineType.PETROL,
    )

    fetched = await repo.get_car_by_id(created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.make == "TestMake"
    assert fetched.engine_type == EngineType.PETROL


async def test_update(db_session):
    repo = CarRepository(db_session)

    created = await repo.create_car(
        make="TestMake",
        model="ToUpdate",
        year=2019,
        color="Blue",
        price=11111.11,
        engine_type=EngineType.DIESEL,
    )

    updated = await repo.update_car(
        created.id,
        color="Green",
        price=22222.22,
        engine_type=EngineType.HYBRID.value,
    )

    assert updated is not None
    assert updated.color == "Green"
    assert updated.price == 22222.22
    assert updated.engine_type == EngineType.HYBRID


async def test_delete(db_session):
    repo = CarRepository(db_session)

    created = await repo.create_car(
        make="ToDelete",
        model="ModelX",
        year=2018,
        color="Black",
        price=9999.99,
        engine_type=EngineType.PETROL,
    )

    await repo.delete_car(created.id)

    fetched = await repo.get_car_by_id(created.id)
    assert fetched is None


async def test_list_count(db_session):
    repo = CarRepository(db_session)

    cars = await repo.list_cars()
    assert len(cars) == 0

    await repo.create_car(
        make="Make1",
        model="Model1",
        year=2021,
        color="White",
        price=10000.0,
        engine_type=EngineType.PETROL,
    )
    await repo.create_car(
        make="Make2",
        model="Model2",
        year=2022,
        color="Blue",
        price=20000.0,
        engine_type=EngineType.ELECTRIC,
    )

    cars = await repo.list_cars()
    assert len(cars) == 2
