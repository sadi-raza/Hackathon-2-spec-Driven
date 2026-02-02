"""
Script to drop and recreate all tables with integer IDs.

This is needed because we changed from UUID to auto-increment integer IDs.
"""

import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.models.user import User
from app.models.task import Task
from app.models.conversation import Conversation
from app.models.message import Message
from sqlmodel import SQLModel


async def recreate_tables():
    """Drop and recreate all tables."""
    print(f"Connecting to database...")
    print(f"DATABASE_URL: {settings.DATABASE_URL[:50]}...")

    engine = create_async_engine(settings.DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        print("\n=== Dropping existing tables ===")
        # Drop tables in correct order (respect foreign key constraints)
        await conn.execute(text("DROP TABLE IF EXISTS messages CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS conversations CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        print("Tables dropped successfully!")

        print("\n=== Creating new tables ===")
        # Create all tables with new schema
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Tables created successfully!")

    await engine.dispose()
    print("\n=== Migration completed! ===")


if __name__ == "__main__":
    asyncio.run(recreate_tables())
