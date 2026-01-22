from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your actual Postgres credentials
DATABASE_URL = "postgresql+asyncpg://postgres:1234567890@localhost:5432/appointment_db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Generator for efficient session handling
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session