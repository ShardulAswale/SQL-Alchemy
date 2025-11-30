import asyncio

from db_example.models.car import EngineType
from db_example.uow.car_uow import CarUnitOfWork


async def main() -> None:
    print(">>> demo_crud starting")

    # 1. Create a car
    async with CarUnitOfWork() as uow:
        car = await uow.cars.create_car(
            make="DemoMake",
            model="DemoModel",
            year=2024,
            color="Green",
            price=25000.0,
            engine_type=EngineType.PETROL,
        )
        print(f"[CREATE] Created car: {car}")

    # 2. Fetch the car
    async with CarUnitOfWork() as uow:
        fetched = await uow.cars.get_car_by_id(car.id)
        print(f"[READ] Fetched car: {fetched}")

    # 3. Update the car
    async with CarUnitOfWork() as uow:
        updated = await uow.cars.update_car(
            car.id,
            color="Yellow",
            price=26000.0,
        )
        print(f"[UPDATE] Updated car: {updated}")

    # 4. List all cars
    async with CarUnitOfWork() as uow:
        cars = await uow.cars.list_cars()
        print(f"[LIST] All cars ({len(cars)}):")
        for c in cars:
            print("   ", c)

    # 5. Delete the demo car
    async with CarUnitOfWork() as uow:
        await uow.cars.delete_car(car.id)
        print(f"[DELETE] Deleted car with id={car.id}")

    # 6. Confirm deletion
    async with CarUnitOfWork() as uow:
        deleted = await uow.cars.get_car_by_id(car.id)
        print(f"[READ AFTER DELETE] Should be None → {deleted}")

    print(">>> demo_crud finished")


if __name__ == "__main__":
    asyncio.run(main())
