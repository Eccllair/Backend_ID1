from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def create_user_table(session: AsyncSession):
    await session.execute(text(
        """
            CREATE TABLE user(
                id SERIAL PRIMARY KEY,
                name VARCHAR(30)
            );
        """
    ))