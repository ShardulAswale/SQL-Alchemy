import asyncio
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

from db_example.db.engine import get_async_engine


async def migrate() -> None:
    """
    Migration to add the engine_type column to the cars table.

    Steps:
    1. Add engine_type (nullable) if it doesn't already exist.
    2. Populate NULL values with 'petrol'.
    3. Change column to NOT NULL with no default.
    """

    engine = get_async_engine()

    async with engine.begin() as conn:

        # 1) Add column if it does not exist
        try:
            await conn.execute(
                text("ALTER TABLE cars ADD COLUMN engine_type VARCHAR(20);")
            )
            print("✔ Added engine_type column (nullable).")
        except ProgrammingError:
            print("ℹ engine_type column already exists, skipping ADD.")

        # 2) Set NULL engine_type values to 'petrol'
        await conn.execute(
            text(
                """
                UPDATE cars
                SET engine_type = 'petrol'
                WHERE engine_type IS NULL;
                """
            )
        )
        print("✔ Populated NULL engine_type values with 'petrol'.")

        # 3) Make column NOT NULL (no default value)
        await conn.execute(
            text(
                """
                ALTER TABLE cars
                MODIFY COLUMN engine_type VARCHAR(20) NOT NULL;
                """
            )
        )
        print("✔ Modified engine_type to NOT NULL.")


async def main() -> None:
    print(">>> Running migration: add engine_type to cars table")
    await migrate()
    print(">>> Migration completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
