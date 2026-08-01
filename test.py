from sqlalchemy import text

from app.core.database import engine

import asyncio

async def main():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT version();"))
        print(result.scalar())

asyncio.run(main())