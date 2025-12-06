import os
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = os.getenv( "DATABASE_URL")

engine = create_async_engine( 
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(  
    bind=engine,
    autoflush=False,  # nie wypycha zmian automatycznie przed SELECT
    expire_on_commit=False,  # po commit obiekty są świeże
    class_=AsyncSession,
)

Base = declarative_base()  # klasa bazowa

async def get_db():  # każdy request ma własną, niezależną sesję do bazy
    async with AsyncSessionLocal() as session:
        yield session
