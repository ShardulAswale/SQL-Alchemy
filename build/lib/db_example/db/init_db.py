import asyncio
import csv
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncEngine

from db_example.db.base import Base
from db_example.db.engine import get_async_engine
from db_example.uow.car_uow import CarUnitOfWork
from db_example.models.car import EngineType, Car


# init_db.py is in: src/db_example/db/init_db.py
# parents: [0]=db, [1]=db_example, [2]=src, [3]=project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "cars.csv"


async def create_tables(engine: AsyncEngine) -> None:
    """Create all tables defined on the Base metadata."""
    # Ensure model is imported so it's registered with Base.metadata
    _ = Car  # noqa: F841
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def load_csv_data() -> int:
    """
    Load data from cars.csv using CarUnitOfWork and CarRepository.
    Returns number of inserted rows.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {DATA_PATH}")

    inserted = 0

    async with CarUnitOfWork() as uow:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Basic validation
                if not row.get("make") or not row.get("model"):
                    continue

                engine_raw = (row.get("engine_type") or "").strip().lower()
                valid_values = {e.value for e in EngineType}
                if engine_raw not in valid_values:
                    engine_raw = "petrol"  # fallback

                engine_type = EngineType(engine_raw)

                await uow.cars.create_car(
                    make=row["make"],
                    model=row["model"],
                    year=int(row["year"]),
                    color=row["color"],
                    price=float(row["price"]),
                    engine_type=engine_type,
                )
                inserted += 1

        # Commit is handled by CarUnitOfWork.__aexit__
    return inserted


async def main() -> None:
    print(">>> init_db.main() starting")
    engine = get_async_engine()
    await create_tables(engine)
    rows = await load_csv_data()
    print(f"✅ Inserted {rows} rows from {DATA_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
